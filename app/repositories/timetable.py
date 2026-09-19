class TimeTableRepository:
    async def fetch(self, conn, fn_name, emp_id=None):
        if fn_name == "timeTable":
            return await conn.fetch("SELECT * FROM timetable")
        return await conn.fetch(
            """SELECT day,period1,period2,period3,period4,period5,period6
            FROM timetable WHERE id=$1""", emp_id
        )

    async def update(self, conn, emp_id, periods):
        for day, values in periods.items():
            if len(values) != 6:
                raise ValueError("Each timetable day must contain 6 periods")
            await conn.execute(
                """UPDATE timetable SET period1=$1,period2=$2,period3=$3,
                period4=$4,period5=$5,period6=$6
                WHERE id=$7 AND day=$8""",
                *values, emp_id, day
            )

timetable_repo = TimeTableRepository()
