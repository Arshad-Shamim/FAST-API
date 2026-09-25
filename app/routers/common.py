from fastapi import APIRouter, Depends, Response, HTTPException, File, UploadFile, Form
from app.db.database import get_pool
from app.dependencies.auth import authentication
from app.schemas.common import SignIn, Signup
from app.services.auth_service import signin
from app.services.common_service import home, signup, leave_history, upload
from datetime import date

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

@router.post("/file")
# async def upload_file(file_title:str=Form(...),receivers:list[str]=Form(...),file: UploadFile=File(...), identity=Depends(authentication)):
async def upload_file(user_id:str=Form(...),file_title:str=Form(...),receivers:list[str]=Form(...),file: UploadFile=File(...)):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await upload(conn,user_id=user_id,file=file,file_title=file_title,receivers=receivers)
