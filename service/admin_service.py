from datetime import datetime
import bcrypt
from model.users import users_repo
from model.users_leave_history import history_repo
from model.users_leave_status import status_repo
from model.time_table import timetable_repo
from utils.dates import increase_dates, count_days_between_dates

async def add_teacher(conn, data):
    data = data.copy()
    data["pws"] = bcrypt.hashpw(data["name"].encode(), bcrypt.gensalt(rounds=5)).decode()
    return await users_repo.add_teacher(conn, data)

async def pending(conn):
    rows = await history_repo.fetch(conn, "pendingApplications")
    return {"status":1,"msg":"Success","data":increase_dates(rows,["application_date"])}

async def application_details(conn, application_id):
    rows = await history_repo.fetch(conn, "applicationDetails", application_id=application_id)
    if not rows:
        raise RuntimeError("Server Error!")
    details = increase_dates(rows,["application_date","start_date","end_date"])[0]
    report = await status_repo.fetch(conn, "applicationDetails", id=details["emp_id"])
    return {"status":1,"data":{"application_details":details,
                              "leave_report":dict(report[0]) if report else None},
            "msg":"success"}

async def application_response(conn, response, application_data):
    days = count_days_between_dates(application_data["start_date"], application_data["end_date"]) + 1
    rowcount = await history_repo.update_response(conn, response, application_data["leave_id"])
    if str(rowcount).endswith("0"):
        return {"status":0,"msg":"Invalid Application"}
    await status_repo.update(conn, "applicationResponse",
                             emp_id=application_data["emp_id"],
                             type=application_data["type"], days=days)
    return {"status":"Response Submitted!"}

async def teachers(conn):
    rows = await users_repo.fetch(conn, "teachersList")
    return {"status":1,"msg":"Success","data":[dict(x) for x in rows]}

async def update_timetable(conn, emp_id, periods):
    await timetable_repo.update(conn, emp_id, periods)
    return {"status":1,"msg":"Time Table Updated"}

async def get_timetable(conn, emp_id):
    rows = await timetable_repo.fetch(conn, "getTimeTable", emp_id)
    table = {}
    for x in rows:
        table[x["day"]] = [x["period1"],x["period2"],x["period3"],x["period4"],x["period5"],x["period6"]]
    return {"status":1,"data":table,"msg":"Data Fteched Successfully!"}

async def substitution(conn, date_value, absent_teachers):
    priority_rows = await status_repo.fetch(conn, "timeTable")
    table_rows = await timetable_repo.fetch(conn, "timeTable")
    teacher_rows = await users_repo.fetch(conn, "timeTable", ["id","name"])
    if not priority_rows:
        return {"status":0,"msg":"Empty users"}
    if not table_rows:
        return {"status":0,"msg":"Empty Time Table"}
    if not teacher_rows:
        return {"status":0,"msg":"No Teacher added!"}

    priority = [dict(x) for x in priority_rows]
    table = {f"{x['id']}{x['day']}":[x["period1"],x["period2"],x["period3"],x["period4"],x["period5"],x["period6"]] for x in table_rows}
    teachers = {str(x["id"]):x["name"] for x in teacher_rows}
    absent = list(absent_teachers)
    dt = datetime.fromisoformat(date_value.replace("Z","+00:00"))
    day = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][(dt.weekday()+1)%7]
    result = {}

    for emp_id in absent:
        emp_id = str(emp_id)
        if emp_id not in teachers:
            continue
        own = table.get(f"{emp_id}{day}")
        if own is None:
            continue
        output = []
        for c in range(6):
            if own[c] == "null":
                output.append("NA")
                continue
            found = False
            for i, candidate in enumerate(priority):
                cid = str(candidate["id"])
                if cid == emp_id:
                    continue
                candidate_table = table.get(f"{cid}{day}")
                if candidate_table and candidate_table[c] == "null" and cid not in absent:
                    output.append(teachers[cid])
                    candidate_table[c] = "SUB"
                    priority.append(priority.pop(i))
                    found = True
                    break
            if not found:
                output.append("Libary")
        result[teachers[emp_id]] = output

    await status_repo.update(conn, "timeTable", priorityArray=priority)
    return {"status":1,"data":result,"msg":"Table generated successfully"}
