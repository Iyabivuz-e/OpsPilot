from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
# from pydantic import BaseModel
# from services.user.user import get_all_user, get_user 
from services.user.user import get_all_users, get_user

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/", status_code=200)
async def employees(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db=db)

@router.get("/{user_id}", status_code=200)
async def employees(user_id: str, db: AsyncSession = Depends(get_db)):
    return await get_user(user_id=user_id, db=db)