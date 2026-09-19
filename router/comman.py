from fastapi import APIRouter, Depends, Response, HTTPException
from model.database import get_pool
from middleware.common import authentication
from schema.common import SignIn, Signup
from service.auth_service import signin
from service.common_service import home, signup, leave_history

router = APIRouter()

@router.post("/signin")
async def sign_in(data: SignIn, response: Response):
    pool = await get_pool()
    async with pool.acquire() as conn:
        token, body, code = await signin(conn, data)
    if code != 200:
        response.status_code = code
        return body
    response.set_cookie("token", token, httponly=True,
                        secure=True, max_age=7*24*60*60, samesite="none")
    return body

@router.get("/home")
async def get_home(identity=Depends(authentication)):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await home(conn, identity["email"], identity["role"])

@router.post("/user")
async def store_signup(data: Signup):
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await signup(conn, data.model_dump())
    return result

@router.get("/leave_history")
async def get_leave_history(identity=Depends(authentication)):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await leave_history(conn, identity["email"], identity["role"])
