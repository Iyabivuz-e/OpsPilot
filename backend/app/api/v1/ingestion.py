from fastapi import APIRouter, UploadFile, Depends
from services.ingestion import ingest_documents
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db


router = APIRouter(prefix="/api/v1/ingestion", tags=["ingestion"])


@router.post("/ingest", status_code=201)
async def ingest_docs(
    doc: UploadFile, 
    category: str, 
    department: str, 
    db: AsyncSession = Depends(get_db)):
    
    return await ingest_documents(doc, category, department, db)