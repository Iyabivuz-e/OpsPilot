from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from models.models import User
from sqlalchemy import select


async def get_all_users(
    skip:int = 0, limit:int = 50,
    db: AsyncSession = Depends(get_db)):
    """
    Retrieve all users.
    """
    stmt = select(User).offset(skip).limit(limit)
    results = await db.scalars(stmt)
    customers = results.all()
    
    if not customers:
        raise HTTPException(status_code=404, detail="Oops, we didn't find any ):")
    return customers

async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a user by their ID.
    """
    stmt = select(User).where(User.id == user_id)
    customer = await db.scalar(stmt)
    if not customer:
        raise HTTPException(status_code=404, detail="User not found")
    return customer
