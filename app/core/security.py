from jose import jwt
from app.core.config import JWT_SECRET, JWT_ALGORITHM


def create_token(data: dict) -> str:
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is not configured")
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is not configured")
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
