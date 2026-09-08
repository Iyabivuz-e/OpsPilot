from sqlalchemy import select
from models.models import User, Customer
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schema import Login
from core.settings import settings
from helpers.errors import UserNotFoundError
from fastapi import HTTPException

async def login(email: str, db: AsyncSession) -> Login:
    
    if not email:
        raise HTTPException(status_code=404, detail="input is missing")
    
    if email.endswith(settings.DOMAIN_NAME.lower()):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
    else:
        result = await db.execute(select(Customer).where(Customer.email == email))
        user = result.scalar_one_or_none()

    if not user:
        raise UserNotFoundError()

    return user
