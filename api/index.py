from fastapi import FastAPI
from router.comman import router as common_router
from router.admin import router as admin_router
from router.user import router as user_router

app = FastAPI(title="Leave Manager API")

@app.get("/")
async def root():
    return "hello world!"

app.include_router(common_router)
app.include_router(admin_router, prefix="/admin")
app.include_router(user_router, prefix="/user")
