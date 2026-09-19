from fastapi import HTTPException, Request
from app.core.security import verify_token
from app.db.database import get_pool
from app.repositories.users import users_repo


async def authentication(request: Request):
    token = request.cookies.get("token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail={"status": 0, "msg": "Please login!"},
        )

    try:
        payload = verify_token(token)
        email = payload["email"]
        role = payload["role"]

        pool = await get_pool()
        async with pool.acquire() as conn:
            rows = await users_repo.fetch(
                conn, "authentication", ["email"], email
            )

        if not rows:
            raise ValueError("Email not found")

        return {"email": email, "role": role}

    except Exception:
        raise HTTPException(
            status_code=401,
            detail={"status": 0, "msg": "Please login!"},
        )
