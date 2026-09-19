from fastapi import Depends, HTTPException
from app.dependencies.auth import authentication


async def administrator(identity=Depends(authentication)):
    if identity["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail={"status": 0, "msg": "only Admin Perform this Action!"},
        )
    return identity


async def employee(identity=Depends(authentication)):
    if identity["role"] != "employee":
        raise HTTPException(
            status_code=403,
            detail={"status": 0, "msg": "only Employee Perform this Action!"},
        )
    return identity
