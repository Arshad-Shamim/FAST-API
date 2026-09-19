from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import FRONTEND_ORIGIN
from app.routers import admin, common, user


def create_app() -> FastAPI:
    application = FastAPI(
        title="Leave Manager API",
        version="1.0.0",
    )

    origins = ["*"] if FRONTEND_ORIGIN == "*" else [FRONTEND_ORIGIN]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(common.router)
    application.include_router(admin.router, prefix="/admin")
    application.include_router(user.router, prefix="/user")

    return application


app = create_app()
