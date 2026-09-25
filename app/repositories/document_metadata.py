class DocumentMetadataRepository:

    async def fetch(self, conn, fn_name, **p):

        if fn_name == "upload":
            return await conn.fetch(
                """
                SELECT user_id, file_title, date, size
                FROM "DOCUMENTS-METADATA"
                WHERE user_id=$1
                ORDER BY date DESC
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