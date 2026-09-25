import bcrypt
from app.repositories.users import users_repo
from app.repositories.leave_history import history_repo
from app.utils.dates import increase_dates
from fastapi import UploadFile, File, HTTPException, Form
from app.db.database import supabase
from datetime import date
from app.repositories.document_metadata import document_metadata_repo
from app.repositories.documents_receivers import document_receivers


async def home(conn, email, role):
    rows = await users_repo.fetch(conn, "getHome", ["*"], email)
    if not rows:
        raise RuntimeError("Server Error!")
    data = dict(rows[0])
    data.pop("password", None)
    return {"status":1,"userInfo":data,"role":role}

async def signup(conn, data):
    hashed = bcrypt.hashpw(data["pws"].encode(), bcrypt.gensalt(rounds=5)).decode()
    data = data.copy()
    data["password"] = hashed
    try:
        await users_repo.signup(conn, data)
        return {"status":1}
    except Exception as e:
        if getattr(e, "sqlstate", None) == "23505":
            return {"status":0,"msg":"Duplicate email or id!"}
        raise

async def leave_history(conn, email, role):
    rows = await history_repo.fetch(conn, "leaveHistory", email=email, role=role)
    rows = increase_dates(rows, ["application_date","start_date","end_date"])
    return {"status":1,"data":rows,"msg":"success","role":0 if role=="employee" else 1}

async def upload(conn,user_id: str, file: UploadFile, file_title:str=Form(...), receivers: list[str]=Form(...)):

    try:
        file_content = await file.read()

        storage_path = f"{user_id}/{file.filename}"

        response = supabase.storage \
            .from_("documents") \
            .upload(
                storage_path,
                file_content,
                {
                    "content-type": file.content_type
                }
            )

        file_size = len(file_content)


        data = {
            "user_id": user_id,
            "file_title": file_title,
            "size": file_size,
            "date": date.today(),
            "file_path":storage_path
        }


        res1 = await document_metadata_repo.store(
            conn=conn,
            data=data,
            fn_name="upload"
        )

        for receiver in receivers:
            data2 = {
                "file_title":file_title,
                "receiver":receiver,
                "user_id":user_id
            }
            res2 = await document_receivers.store(fn="upload",conn=conn,data=data2)
            print(res2)

        return {
            "message": "File uploaded successfully",
            "file_name": file.filename,
            "storage_path": storage_path
        }

    except Exception as e:
        print("File upload error:", e)
        import traceback
        traceback.print_exc()
        return {
            "message": "File upload failed",
            "error": str(e)
        }

