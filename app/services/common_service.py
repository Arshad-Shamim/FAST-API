import bcrypt
from app.repositories.users import users_repo
from app.repositories.leave_history import history_repo
from app.utils.dates import increase_dates

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
