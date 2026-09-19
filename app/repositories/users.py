class UsersRepository:
    async def fetch(self, conn, fn_name, fields=None, email=None):
        if fn_name in ("getHome", "signIn", "authentication"):
            columns = ",".join(fields or ["*"])
            return await conn.fetch(f"SELECT {columns} FROM users WHERE email=$1", email)
        if fn_name == "timeTable":
            columns = ",".join(fields or ["*"])
            return await conn.fetch(f"SELECT {columns} FROM users")
        if fn_name == "teachersList":
            return await conn.fetch(
                "SELECT name,email,designation,photo,id,department,joining FROM users"
            )
        return []

    async def signup(self, conn, data):
        # Original signup intends to create a user. Uses explicit columns rather
        # than fragile positional INSERT syntax.
        return await conn.execute(
            """INSERT INTO users
            (email,password,id,name,role,designation,photo,department,joining)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)""",
            data["email"], data["password"], data.get("id"), data.get("name"),
            data.get("role", "employee"), data.get("designation"),
            data.get("photo"), data.get("department"), data.get("joiningDate")
        )

    async def add_teacher(self, conn, data):
        return await conn.execute(
            """INSERT INTO users
            (email,password,id,name,role,designation,photo,department,joining)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)""",
            data["email"], data["pws"], data["empId"], data["name"],
            data["role"], data["designation"], data["photo"],
            data["department"], data["joiningDate"]
        )

users_repo = UsersRepository()
