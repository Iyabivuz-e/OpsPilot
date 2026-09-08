from fastapi import APIRouter, Depends, HTTPException

# from schemas.schema import User
from auth.login import login
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from auth.jwt_token import create_jwt
from schemas.schema import LoginRequest
from helpers.errors import InvalidCredentialsError

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login")
async def handle_login(data: LoginRequest , session: AsyncSession = Depends(get_db)):
    user = await login(data.email, session)

    if not user:
        raise InvalidCredentialsError()

    token = await create_jwt(user)

    return token


@router.get("/logout")
async def handle_logout():
    # Implement logout logic here (e.g., invalidate the token)
    return {"message": "Logged out successfully"}