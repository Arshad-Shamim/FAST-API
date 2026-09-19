from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.index import app as api_app
from config import FRONTEND_ORIGIN

app = FastAPI(title="Leave Manager API")
origins = ["*"] if FRONTEND_ORIGIN == "*" else [FRONTEND_ORIGIN]
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["GET","POST","PUT","DELETE","OPTIONS"],
                   allow_headers=["*"])
app.mount("", api_app)
