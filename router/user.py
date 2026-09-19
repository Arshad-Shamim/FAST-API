from fastapi import APIRouter, Depends
from model.database import get_pool
from middleware.common import authentication
from middleware.user import user_auth
from schema.leave import Application
from service.user_service import submit_application

router = APIRouter()

async def employee(identity=Depends(authentication)):
    return user_auth(identity)

@router.post("/application")
async def application(data: Application, identity=Depends(employee)):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await submit_application(conn, identity["email"], data.model_dump())
