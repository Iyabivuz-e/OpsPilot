import time
import jwt
from uuid import UUID
from core.settings import settings



async def create_jwt(user: str):
    payload = {"user_id": str(user.id), "expires": time.time() + 3600}

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    return {"access_token": token}


async def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            UUID(token), settings.JWT_SECRET, algorithm=[settings.JWT_ALGORITHM]
        )
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        return e
