from core.settings import settings
import time
import jwt


async def create_jwt(user: str):
    payload = {"user_id": user.id, "expires": time.time() + 3600}

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    return {"access_token": token}


async def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET, algorithm=[settings.JWT_ALGORITHM]
        )
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
