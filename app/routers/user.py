from fastapi import APIRouter, Depends
from app.db.database import get_pool
from app.dependencies.auth import authentication
from app.dependencies.roles import employee
from app.schemas.leave import Application
from app.services.user_service import submit_application

router = APIRouter()


@router.post("/application")
async def application(data: Application, identity=Depends(employee)):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await submit_application(conn, identity["email"], data.model_dump())
