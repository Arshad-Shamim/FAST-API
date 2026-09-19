class LeaveHistoryRepository:
    async def fetch(self, conn, fn_name, **p):
        if fn_name == "submitApplication":
            return await conn.fetch(
                "SELECT start_date,end_date FROM users_leave_history "
                "WHERE start_date <= $1 AND end_date >= $2",
                p["endDate"], p["startDate"]
            )
        if fn_name == "leaveHistory":
            if p["role"] == "employee":
                return await conn.fetch(
                    "SELECT * FROM users_leave_history WHERE email=$1", p["email"]
                )
            return await conn.fetch(
                """SELECT history.leave_id,history.application_date,history.type,
                history.purpose,history.start_date,history.end_date,history.status,
                users.id,users.name FROM users_leave_history history
                LEFT JOIN users ON users.email=history.email
                WHERE history.status!='pending' ORDER BY history.leave_id DESC"""
            )
        if fn_name == "pendingApplications":
            return await conn.fetch(
                """SELECT history.leave_id,history.emp_id,users.name,
                history.application_date FROM users
                JOIN users_leave_history history ON users.email=history.email
                WHERE history.status='pending'"""
            )
        if fn_name == "applicationDetails":
            return await conn.fetch(
                """SELECT history.leave_id,history.emp_id,history.application_date,
                history.type,history.purpose,history.start_date,history.end_date,
                users.name,users.department FROM users_leave_history history
                LEFT JOIN users ON users.email=history.email
                WHERE history.leave_id=$1""", p["application_id"]
            )
        if fn_name == "timeTable":
            return await conn.fetch(
                """SELECT emp_id,start_date,end_date FROM users_leave_history
                WHERE NOT(start_date <= $1 AND end_date <= $1
                OR start_date >= $2 AND end_date >= $2)
                AND start_date>'2025-07-08'""", p["startDate"], p["endDate"]
            )
        return []

    async def store(self, conn, data):
        return await conn.execute(
            """INSERT INTO users_leave_history
            (email,application_date,type,purpose,start_date,end_date,status)
            VALUES ($1,$2,$3,$4,$5,$6,$7)""",
            data["email"], data["applicationDate"], data["type"],
            data["purpose"], data["startDate"], data["endDate"], data["status"]
        )

    async def update_response(self, conn, response, leave_id):
        status = "reject" if response == 0 else "approved"
        return await conn.execute(
            "UPDATE users_leave_history SET status=$1 WHERE leave_id=$2",
            status, leave_id
        )

history_repo = LeaveHistoryRepository()
