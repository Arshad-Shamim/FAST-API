import asyncpg
from app.core.config import (
    DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD, DB_SSL
)

_pool = None


async def get_pool():
    global _pool

    if _pool is None:
        kwargs = {
            "host": DB_HOST,
            "port": DB_PORT,
            "user": DB_USER,
            "database": DB_NAME,
            "password": DB_PASSWORD,
            "min_size": 1,
            "max_size": 10,
        }

        if DB_SSL:
            kwargs["ssl"] = "require"

        _pool = await asyncpg.create_pool(**kwargs)

    return _pool


async def close_pool():
    global _pool

    if _pool is not None:
        await _pool.close()
        _pool = None
