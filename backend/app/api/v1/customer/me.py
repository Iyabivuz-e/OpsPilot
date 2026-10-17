from fastapi import APIRouter, Depends
from helpers.current_logged import get_current_user

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])

@router.get("/me", status_code=200)
async def get_me(current_user = Depends(get_current_user)):
    return current_user
