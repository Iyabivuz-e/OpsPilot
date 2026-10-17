import time
import jwt
from uuid import UUID
from core.settings import settings



async def create_jwt(user: str):
    payload = {
        "user_id": str(user.id), 
        "exp": time.time() + 3600}

    token = jwt.encode(
        payload, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALGORITHM)

    return {"access_token": token}


async def decode_jwt(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
        
        # return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.InvalidTokenError as e :
        print(f"JWT decode failed: {type(e).__name__}: {e}")
        return None
