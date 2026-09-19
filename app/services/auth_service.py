import bcrypt
from fastapi import HTTPException
from app.repositories.users import users_repo
from app.core.security import create_token

async def signin(conn, data):
    rows = await users_repo.fetch(conn, "signIn", ["password","role"], data.email)
    if not rows:
        return None, {"status":0,"msg":"Email not found!"}, 404
    if rows[0]["role"] != data.role:
        return None, {"status":0,"msg":"Please select correct a role!"}, 404
    if not bcrypt.checkpw(data.password.encode(), rows[0]["password"].encode()):
        return None, {"status":0,"msg":"Incorrect password!"}, 401
    # Preserve Node behavior: token is NOT returned in JSON; it is a cookie.
    token = create_token({"email": data.email, "role": data.role})
    return token, {"status":1,"msg":"Authentication Successful!"}, 200
