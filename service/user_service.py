from model.users_leave_history import history_repo
from model.users_leave_status import status_repo

async def submit_application(conn, email, data):
    data = data.copy()
    data["email"] = email
    data["pupose"] = data.get("purpose") if data.get("purpose") else "null"
    # Preserve intended DB field name while fixing the original typo.
    data["purpose"] = data["pupose"]
    data["status"] = "pending"

    rows = await history_repo.fetch(conn, "submitApplication",
                                    startDate=data["startDate"], endDate=data["endDate"])
    if rows:
        return {"status":0,"msg":"Leave Period Conflig"}

    if data["type"] in ("CL","ML"):
        balances = await status_repo.fetch(conn, "submitApplication",
                                           type=data["type"], email=email)
        if not balances:
            return {"status":0,"msg":"DB Error!"}
        balance = balances[0][f"{data['type'].lower()}_balance"]
        if balance < data["days"]:
            return {"status":0,"msg":f"Does't enough {data['type']} Leave Balance!"}

    await history_repo.store(conn, data)
    return {"status":1,"msg":"Application Submited!"}
