class DocumentMetadataRepository:

    async def fetch(self, conn, fn_name, **p):

        if fn_name == "upload":
            return await conn.fetch(
                """
                SELECT 
                    t1.user_id,
                    t1.file_title,
                    t1.date,
                    t1.size,
                    t1.file_path,
                    ARRAY_AGG(t2.receiver) AS receivers
                FROM "DOCUMENTS-METADATA" AS t1
                JOIN "DOCUMENT-RECEIVERS" AS t2
                    ON t1.user_id = t2.user_id
                    AND t1.file_title = t2.file_title
                WHERE t1.user_id = $1
                GROUP BY
                    t1.user_id,
                    t1.file_title,
                    t1.date,
                    t1.size,
                    t1.file_path
                ORDER BY t1.date DESC
                """,
                p["user_id"]
            )

        return []

    async def store(self, conn, data, fn_name):

        if fn_name == "upload":
            return await conn.execute(
                """
                INSERT INTO "DOCUMENTS-METADATA"
                (user_id, file_title, date, size, file_path)
                VALUES ($1, $2, $3, $4, $5)
                """,
                data["user_id"],
                data["file_title"],
                data["date"],
                data["size"],
                data["file_path"]
            )
        print("Unexcepted error")
        return "Unexcepted error"


document_metadata_repo = DocumentMetadataRepository()