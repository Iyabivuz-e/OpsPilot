from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
# from pydantic import BaseModel
from services.chat.chat import completion


router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/chat", status_code=201)
async def chat(query: str, db: AsyncSession = Depends(get_db)):
    return await completion(query=query, db=db)