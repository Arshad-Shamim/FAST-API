class HolidaysRepository:
    async def fetch(self, conn, start_date):
        return await conn.fetch(
            "SELECT date::DATE,name FROM holidays WHERE date >= $1", start_date
        )

holidays_repo = HolidaysRepository()
