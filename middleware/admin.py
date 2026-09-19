from fastapi import HTTPException

def admin_auth(identity):
    if identity["role"] != "admin":
        raise HTTPException(status_code=200, detail={"status":0,"msg":"only Admin Perform this Action!"})
    return identity
