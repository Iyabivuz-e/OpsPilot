from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
# from pydantic import BaseModel
from services.chat.conversation import create_conversation, get_conversations
from models.models import Customer
from helpers.current_logged import get_current_user



router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


## Create a conversation
@router.post("/", status_code=201)
async def chat(
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a chat response based on the provided prompt.
    """
    response = await create_conversation(user_id=current_user, db=db)
    
    if not response:
        raise HTTPException(
            status_code=404, 
            detail="No conversations found for the current user.")
    return {
        "message": "Conversation created successfully.",
        "conversation": response
        }


# Get all chats for the current user
@router.get("/chats", status_code=200)
async def handle_get_chats(
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a chat response based on the provided prompt.
    """
    response = await get_conversations(current_user=current_user, db=db)
    
    if not response:
        raise HTTPException(
            status_code=404, 
            detail="No conversations found for the current user.")
    return response