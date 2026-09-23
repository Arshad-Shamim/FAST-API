import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("dbHost", "localhost")
DB_PORT = int(os.getenv("dbPort", "5432"))
DB_USER = os.getenv("user", "postgres")
DB_NAME = os.getenv("database", "leave_manager")
DB_PASSWORD = os.getenv("password", "")
DB_SSL = os.getenv("DB_SSL", "true").lower() == "true"

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")
CLOUDINARY_FOLDER = os.getenv("CLOUDINARY_FOLDER", "Leave-Portal-Users")

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")

DB_URL = os.getenv("SUPABASE_URL","")
DB_API_KEY = os.getenv("SUPABASE_API_KEY","")