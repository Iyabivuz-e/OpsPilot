from fastapi import APIRouter, Depends

# from schemas.schema import User
from auth.login import login
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from http.client import HTTPException
from auth.jwt_token import create_jwt

router = APIRouter(prefix="/api/v1/login")


@router.post("/")
async def handle_login(email: str, session: AsyncSession = Depends(get_db)):
    user = await login(email, session)

    if not user:
        raise HTTPException(status_code=401, details="Invalid credentials")

    token = await create_jwt(user)

    return token
