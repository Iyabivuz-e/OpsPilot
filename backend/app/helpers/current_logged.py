
from auth.jwt_token import decode_jwt
from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from models.models import User
from sqlalchemy import select

async def get_current_user(
    authorization: str = Header(..., description="Authorization header with Bearer token"),
    db: AsyncSession = Depends(get_db)
    ):
    """
    Retrieve the currently logged-in user.
    """
    token = authorization.replace("Bearer ", "", 1)
    print(repr(token))
    
    payload = await decode_jwt(token)
    print(f"Decoded JWT payload: {payload}")  # Debugging line
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    current_user_id = payload.get("user_id")
    print(f"Current user ID: {current_user_id}")  # Debugging line
    
    result = await db.execute(
        select(User).where(User.id == current_user_id))
    
    user = result.scalar_one_or_none()

    
    if not user:
        raise HTTPException(status_code=404, detail="Current user not found")
    
    return user