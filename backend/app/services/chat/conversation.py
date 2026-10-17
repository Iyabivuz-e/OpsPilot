from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from schemas.chat.conversation import ConversationResponse, MessageResponse
from models.models import Conversation, Message, Customer
from uuid import UUID
from helpers.current_logged import get_current_user
from sqlalchemy import select

async def create_conversation(
    user_id: Customer,
    db:AsyncSession = Depends(get_db),
    ) -> ConversationResponse:
    """
    Create a new conversation and return its ID.
    """

    conversation = Conversation(
        user_id=user_id.id,
        title="New Conv", 
        )
    
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    
    return ConversationResponse(
        conversation_id=conversation.id,
        title=conversation.title,
        messages=[],
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )
    
    # return {"conversation_id": new_conversation_id}



### Get all conversations for the current user
async def get_conversations(
    current_user: Customer,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> list[ConversationResponse]:
    """
    Retrieve all conversations for the current user.
    """
    print(f"Fetching the current user  ID: {current_user.id}")  # Debugging line
    results = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    
    conversations = results.scalars().all()
    
    return [
        ConversationResponse(
            conversation_id=conversation.id,
            title=conversation.title,
            messages=[],
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )
        for conversation in conversations
    ]
    
    
##### Get a specific conversation by its ID
async def get_conversation(
    conversation_id: UUID,
    current_user: UUID = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> ConversationResponse:
    """
    Retrieve a conversation by its ID.
    """
    results = await db.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.user_id == current_user.id)
    )
    
    conversation = results.scalar_one_or_none()
    if not conversation:
         raise HTTPException(
             status_code=404, 
             detail="Conversation not found.")
    
    
    results = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc(), Message.id.asc())
        .offset(skip)
        .limit(limit)
    )
    
    messages = results.scalars().all()
    
    message_responses = [
        MessageResponse(
            message_id=message.id,
            content=message.content,
            role=message.role,
            status=message.status,
            created_at=message.created_at,
        )
        for message in messages
    ]

    return ConversationResponse(
        conversation_id=conversation.id,
        title=conversation.title,
        messages=message_responses,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


