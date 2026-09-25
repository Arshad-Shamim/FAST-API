class DOCUMENTSRECEIVERS:

    async def fetch(self, conn, fn_name, **p):

        if fn_name == "upload":
            return await conn.fetch(
                """
                SELECT receivers
                FROM "DOCUMENT-RECEIVERS"
                WHERE user_id=$1
                ORDER BY id DESC
                """,
                p["user_id"]
            )

        return []

    async def store(self, fn,conn, data):
        if fn=="upload":
            print(data["receiver"])
            return await conn.execute(
                """
                INSERT INTO "DOCUMENT-RECEIVERS"
                (file_title, receiver, user_id)
                VALUES ($1, $2, $3)
                """,
                data["file_title"],
                data["receiver"],
                data["user_id"]
            )
        print("documentsreceivers-fail")
        return "documentsreceivers-fail"


document_receivers = DOCUMENTSRECEIVERS()