import os
import shutil
import uuid
import hashlib
from fastapi import UploadFile, HTTPException, Depends
# from database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from core.settings import settings
from rag.chunking.utils import hash_content
from models.models import DocumentModel, DocumentVersion, DocumentStatus
from pathlib import Path
from helpers.document_validator import DocumentValidator
from rag.pipeline import pipeline


validator = DocumentValidator(max_size=int(settings.FILESIZE[:-2]) * 1024 * 1024)  # Convert MB to bytes

async def ingest_documents(doc: UploadFile, category, department, db: AsyncSession):
    
    filesize = settings.FILESIZE
    upload_path = Path(settings.UPLOAD_PATH)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    file_ext = Path(doc.filename).suffix
    filename = Path(doc.filename).name
    # unique_filename = f"{uuid.uuid4()}{file_ext}" ## custom filename to avoid conflicts
    file_path = upload_path / doc.filename
    
    
    if ( doc is None or not category.strip() or not department.strip()):
        raise HTTPException(
            status_code=400, 
            detail={
                "message": "Missing required fields", 
                "errors": ["Document, category, and department are required"]})
    
    
    # Validate the document
    validation = await validator.validate_file(doc)
    if not validation["valid"]:
        raise HTTPException(
            status_code=400, 
            detail = {
                "message": "Document validation failed",
                "errors": validation["errors"]
            }   
    )
        
    try:
        content = await doc.read()
        # content_hash = hash_content(content)
        content_hash = hashlib.sha256(content).hexdigest()  # Compute hash of the content
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to save document: {str(e)}")
        
      
    try:   

        document_model = DocumentModel(
            title=doc.filename,
            category=category,
            department=department,
        )
        db.add(document_model)
        await db.flush() # Ensure the document_model gets an ID before creating the version
            
        document_version = DocumentVersion(
            document_id=document_model.id,
            version_number=1,
            content_hash=content_hash,
            status=DocumentStatus.PROCESSING.value,
            filename=doc.filename,
        )
        
        db.add(document_version)
        await db.flush()  # Ensure the document_version gets an ID before proceeding
        document_model.current_version_id = document_version.id  # Set the current version ID
        
        await db.commit()
        
        saved_chunks = await pipeline(
            file_path=str(file_path), 
            document_version_id=document_version.id, 
            db=db
        )
        
    except Exception as e:
        await db.rollback()
        file_path.unlink(missing_ok=True)  # Remove the file if database operation fails
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to save document metadata: {str(e)}")
        
    
    return {
        
        "message": "Document ingested successfully",
        "document_id": document_model.id,
        "version_id": document_version.version_number,
        "filename": doc.filename,
        "category": category,
        "department": department,
        "content_hash": content_hash
    }
    
    