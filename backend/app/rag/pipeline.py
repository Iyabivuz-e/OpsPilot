import os
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.document_schema import Section
from helpers.mime_types import extension_to_mime
from .extractors.normalizer import normalize_document
from .extractors.registry import registry
from helpers.build_section import build_sections
from .chunking.chunk import chunk_sections 
from .embedding.embedding_worker import embedd_document_task
from core.settings import settings
from .embedding.embedding import Embedding
from models.models import DocumentVersion, DocumentStatus
from uuid import UUID

async def pipeline(file_path: str, document_version_id: UUID, db: AsyncSession) -> list[Section]:

    document_version = await db.get(DocumentVersion, document_version_id)
    
    if document_version is None:
        raise ValueError(f"DocumentVersion with ID {document_version_id} not found.")
    
    extension = os.path.splitext(file_path)[1].lower()
    mime_type = extension_to_mime.get(extension)
    if not mime_type:
        raise ValueError(f"Unsupported file extension: {extension}")
        
    try:
        extractor = registry.get_extractor(mime_type)
        document = extractor.extract(file_path)
        document = normalize_document(document)
        sections = build_sections(document.elements)
        chunks = chunk_sections(
            str(document_version_id), 
            sections)
        # Save the chunks to the database and embed them
        saved_chunks = await embedd_document_task(
            document_version_id=document_version_id, 
            chunks=chunks, 
            db=db
        )
        # Update the document version status to ACTIVE
        document_version.status = DocumentStatus.ACTIVE.value
        
        await db.commit()  # Commit the transaction after saving chunks
        return saved_chunks
    
    except Exception as e:
        await db.rollback()  # Rollback the transaction in case of an error
        raise RuntimeError(f"Error processing document: {e}")
    