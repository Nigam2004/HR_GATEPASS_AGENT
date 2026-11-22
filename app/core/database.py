import sqlite3
from functools import lru_cache

from langgraph.checkpoint.sqlite import SqliteSaver

from app.core.config import DATABASE_PATH


@lru_cache(maxsize=1)
def get_checkpointer() -> SqliteSaver:
    """Create one persistent SQLite checkpointer for LangGraph."""
    connection = sqlite3.connect(
        str(DATABASE_PATH),
        check_same_thread=False,
    )
    checkpointer = SqliteSaver(connection)
    checkpointer.setup()
    return checkpointer


from contextlib import asynccontextmanager

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from app.core.config import DATABASE_PATH


# @asynccontextmanager
# async def get_checkpointer():
#     """Keep the async SQLite checkpointer open while FastAPI is running."""

#     async with AsyncSqliteSaver.from_conn_string(
#         str(DATABASE_PATH)
#     ) as checkpointer:
#         await checkpointer.setup()
#         yield checkpointer
