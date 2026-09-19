from fastapi import UploadFile
import cloudinary
import cloudinary.uploader
from config import CLOUDINARY_CLOUD_NAME,CLOUDINARY_API_KEY,CLOUDINARY_API_SECRET,CLOUDINARY_FOLDER

if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    cloudinary.config(cloud_name=CLOUDINARY_CLOUD_NAME,
                      api_key=CLOUDINARY_API_KEY,
                      api_secret=CLOUDINARY_API_SECRET,
                      secure=True)

async def upload_photo(file: UploadFile):
    content = await file.read()
    result = cloudinary.uploader.upload(
        content, folder=CLOUDINARY_FOLDER,
        allowed_formats=["jpg","png","jpeg"]
    )
    return result["secure_url"]
