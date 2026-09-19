from fastapi import HTTPException

def user_auth(identity):
    if identity["role"] != "employee":
        raise HTTPException(status_code=200, detail={"status":0,"msg":"only Employee Perform this Action!"})
    return identity
