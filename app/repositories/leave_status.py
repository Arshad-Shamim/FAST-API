class LeaveStatusRepository:
    async def fetch(self, conn, fn_name, **p):
        if fn_name == "timeTable":
            return await conn.fetch("SELECT id FROM users_leave_status ORDER BY priority")
        if fn_name == "submitApplication":
            leave_type = p["type"].lower()
            if leave_type not in {"cl","ml"}:
                return []
            return await conn.fetch(
                f"SELECT {leave_type}_balance FROM users_leave_status WHERE email=$1",
                p["email"]
            )
        if fn_name == "applicationDetails":
            return await conn.fetch(
                """SELECT cl_used,ml_used,el_used,lwp_used,
                comp_used,od_used,al_used FROM users_leave_status WHERE id=$1""",
                p["id"]
            )
        return []

    async def update(self, conn, fn_name, **p):
        if fn_name == "applicationResponse":
            leave_type = p["type"].lower()
            used = f"{leave_type}_used"
            allowed = {"cl_used","ml_used","el_used","lwp_used","comp_used","od_used","al_used"}
            if used not in allowed:
                raise ValueError("Invalid leave type")
            if used in {"cl_used", "ml_used"}:
                balance = f"{leave_type}_balance"
                await conn.execute(
                    f"UPDATE users_leave_status SET {balance}={balance}-$1 WHERE id=$2",
                    p["days"], p["emp_id"]
                )
            await conn.execute(
                f"UPDATE users_leave_status SET {used}={used}+$1 WHERE id=$2",
                p["days"], p["emp_id"]
            )
        elif fn_name == "timeTable":
            for i, item in enumerate(p["priorityArray"], 1):
                await conn.execute(
                    'UPDATE users_leave_status SET priority=$1 WHERE id=$2',
                    i, item["id"]
                )

status_repo = LeaveStatusRepository()
