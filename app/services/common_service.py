import bcrypt
from app.repositories.users import users_repo
from app.repositories.leave_history import history_repo
from app.utils.dates import increase_dates
from fastapi import UploadFile, File, HTTPException
from app.db.database import supabase
from datetime import date
from app.repositories.document_metadata import document_metadata_repo
from app.repositories.documents_receivers import document_receivers
import base64
import traceback


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

from fastapi import HTTPException, status

async def upload(
    conn,
    user_id: str,
    file: UploadFile,
    file_title: str,
    receivers: list[str]
):
    try:
        file_content = await file.read()

        storage_path = f"{user_id}/{file_title}"

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
            "file_path": storage_path
        }

        await document_metadata_repo.store(
            conn=conn,
            data=data,
            fn_name="upload"
        )

        for receiver in receivers:
            data2 = {
                "file_title": file_title,
                "receiver": receiver,
                "user_id": user_id
            }

            await document_receivers.store(
                fn="upload",
                conn=conn,
                data=data2
            )

        return {
            "status": 1,
            "msg": "File uploaded successfully",
            "file_name": file.filename,
            "storage_path": storage_path
        }

    except Exception as e:

        traceback.print_exc()
        print(e.__dict__)

        raise HTTPException(
            status_code=int(e.status),
            detail=str(e.message)
        )


async def fetch(conn, user_id: str, role: str):
    response = {
        "status": 0,
        "message": "",
        "send_documents": [],
        "receive_documents": []
    }

    try:
        # --------------------------------------------------
        # Documents uploaded by the user
        # --------------------------------------------------
        res1 = await document_metadata_repo.fetch(
            conn,
            "upload",
            user_id=user_id
        )

        send_documents = []

        for res in res1:

            file_data = None

            if res["file_path"]:
                file_bytes = (
                    supabase.storage
                    .from_("documents")
                    .download(res["file_path"])
                )

                # bytes -> Base64 string
                file_data = base64.b64encode(file_bytes).decode("utf-8")

            send_file_data = {
                "file_title": res["file_title"],
                "date": res["date"].isoformat()
                    if res["date"] else None,
                "size": float(res["size"])
                    if res["size"] is not None else 0,
                "receivers": res["receivers"],
                "file_data": file_data
            }

            send_documents.append(send_file_data)

        response["send_documents"] = send_documents

        # --------------------------------------------------
        # Documents received by the user
        # --------------------------------------------------
        res2 = await document_receivers.fetch(
            conn,
            "upload",
            role=role
        )

        receive_documents = []

        for res in res2:

            file_data = None

            if res["file_path"]:
                file_bytes = (
                    supabase.storage
                    .from_("documents")
                    .download(res["file_path"])
                )

                # bytes -> Base64 string
                file_data = base64.b64encode(file_bytes).decode("utf-8")

            receiver_file_data = {
                "file_title": res["file_title"],
                "date": res["date"].isoformat()
                    if res["date"] else None,
                "size": float(res["size"])
                    if res["size"] is not None else 0,
                "sender": res["sender"],
                "file_data": file_data
            }

            receive_documents.append(receiver_file_data)

        response["receive_documents"] = receive_documents

        response["status"] = 1
        response["msg"] = "Data fetched successfully"

        return response
    
    except Exception as e:

        print("Fetch documents error:", e)
        traceback.print_exc()

        raise HTTPException(
            status_code=int(e.status),
            detail=str(e.message)
        )
