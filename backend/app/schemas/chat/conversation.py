from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class MessageResponse(BaseModel):
    message_id : UUID
    content: str
    role: str
    status: str
    created_at: datetime
    
class ConversationResponse(BaseModel):
    conversation_id: UUID
    messages: list[MessageResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime