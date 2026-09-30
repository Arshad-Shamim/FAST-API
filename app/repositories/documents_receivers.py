class DOCUMENTSRECEIVERS:

    async def fetch(self, conn, fn_name, **p):

        if fn_name == "upload":
            return await conn.fetch(
                """
                SELECT 
                    t1.file_title,
                    t2.date,
                    t2.size,
                    t2.file_path,
                    t1.user_id as sender
                FROM "DOCUMENT-RECEIVERS" AS t1
                RIGHT JOIN "DOCUMENTS-METADATA" AS t2
                    ON t1.user_id = t2.user_id
                    AND t1.file_title = t2.file_title
                WHERE t1.receiver = $1
                """,
                p["role"]
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