from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
# from pydantic import BaseModel
from services.chat.conversation import create_conversation, get_conversations, get_conversation
from models.models import Customer
from helpers.current_logged import get_current_user
from schemas.chat.conversation import ChatRequest
from services.chat.generate import generate_answers
from models.models import Conversation
1

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/stream")
async def stream_chat_response(
    payload: ChatRequest,
    current_user: Customer = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Stream chat responses based on the provided query and conversation history.
    """
    from services.chat.generate import generate_answers

    # Ensure the user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Check if the user has wtitten anything.
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if not payload.model:
        raise HTTPException(status_code=400, detail="The model is missing.")

    # Get the conversation id to be checked against the use when streaming
    if payload.conversation_id is not None:
        conv = await get_conversation(
            conversation_id=payload.conversation_id, 
            current_user=current_user,
            db=db)
        
    if not conv:
        raise HTTPException(status_code=404, detail="The conversation cannot be found")
    else:
        # Create a new conversation for the user -- this will be used when streaming
        conv = Conversation(
            user_id=current_user.id,
            title="New Conv"
        )
        
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        
    # Get the history conversation of the current user.    
    conversation_history = await get_conversations(
        current_user=current_user, 
        db=db
    )
    
    print(f"Conversation history: {conversation_history}")
    
    # Return a streaming response
    return StreamingResponse(
        generate_answers(
            query=payload.message, 
            conversation_history=conversation_history
        ),
        media_type="text/event-stream",
        headers={
            "X-Conversation-ID": str(conv.id),
        },
    ),
    

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