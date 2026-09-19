from fastapi import Request, Response
from auth import verify_token
from model.database import get_pool
from model.users import users_repo

async def authentication(request: Request):
    token = request.cookies.get("token")
    try:
        payload = verify_token(token)
        email = payload["email"]
        role = payload["role"]
        pool = await get_pool()
        async with pool.acquire() as conn:
            rows = await users_repo.fetch(conn, "authentication", ["email"], email)
        if not rows:
            raise ValueError("Email not found")
        return {"email": email, "role": role}
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=201, detail={"status":0,"msg":"Please login!"})
