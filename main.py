# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from api.index import app as api_app
# from config import FRONTEND_ORIGIN

# app = FastAPI(title="Leave Manager API")
# origins = ["*"] if FRONTEND_ORIGIN == "*" else [FRONTEND_ORIGIN]
# app.add_middleware(CORSMiddleware, allow_origins=origins,
#                    allow_credentials=True,
#                    allow_methods=["GET","POST","PUT","DELETE","OPTIONS"],
#                    allow_headers=["*"])
# app.mount("", api_app)

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
