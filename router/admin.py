from fastapi import APIRouter, Depends, File, Form, UploadFile, Query
from model.database import get_pool
from middleware.common import authentication
from middleware.admin import admin_auth
from service.admin_service import add_teacher,pending,application_details,application_response,teachers,substitution,update_timetable,get_timetable
from service.cloudinary_service import upload_photo
from schema.leave import ApplicationResponse
from schema.timetable import TimeTable

router = APIRouter()

async def administrator(identity=Depends(authentication)):
    return admin_auth(identity)

@router.post("/teacher")
async def teacher(identity=Depends(administrator), photo: UploadFile=File(...),
                  email:str=Form(...), empId:str=Form(...), name:str=Form(...),
                  designation:str=Form(...), department:str=Form(...),
                  joiningDate:str=Form(...)):
    photo_url = await upload_photo(photo)
    pool = await get_pool()
    async with pool.acquire() as conn:
        try:
            await add_teacher(conn, {"photo":photo_url,"role":"employee","email":email,
                "empId":empId,"name":name,"designation":designation,
                "department":department,"joiningDate":joiningDate})
        except Exception as e:
            if getattr(e,"sqlstate",None)=="23505":
                return {"status":0,"msg":"Duplicate email or id!"}
            return {"status":0,"msg":"DB Error!"}
    return {"status":1,"msg":"Teacher Added Successfully"}

@router.get("/pending-applications")
async def pending_route(identity=Depends(administrator)):
    pool=await get_pool()
    async with pool.acquire() as conn: return await pending(conn)

@router.get("/application")
async def application_route(application_id:int=Query(...), identity=Depends(administrator)):
    pool=await get_pool()
    async with pool.acquire() as conn: return await application_details(conn,application_id)

@router.put("/application-response")
async def response_route(data:ApplicationResponse, identity=Depends(administrator)):
    pool=await get_pool()
    async with pool.acquire() as conn: return await application_response(conn,data.response,data.applicationData)

@router.get("/teachers")
async def teachers_route(identity=Depends(administrator)):
    pool=await get_pool()
    async with pool.acquire() as conn: return await teachers(conn)

@router.get("/substitution")
async def substitution_route(date:str, absentTeachers:str="", identity=Depends(administrator)):
    pool=await get_pool()
    absent = absentTeachers.split(",") if absentTeachers else []
    async with pool.acquire() as conn: return await substitution(conn,date,absent)

@router.put("/time-table")
async def timetable_route(data:TimeTable):
    pool=await get_pool()
    async with pool.acquire() as conn: return await update_timetable(conn,data.empId,data.periods)

@router.get("/time-table")
async def get_timetable_route(empId:str):
    pool=await get_pool()
    async with pool.acquire() as conn: return await get_timetable(conn,empId)
