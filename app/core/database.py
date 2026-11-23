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

# from collections.abc import AsyncIterator
# from contextlib import asynccontextmanager

# from fastapi import FastAPI
# from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# from app.core.config import DATABASE_PATH

# _checkpointer: AsyncSqliteSaver | None = None


# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncIterator[None]:
#     """Create and manage one async SQLite checkpointer for the app lifetime."""
#     global _checkpointer
#     async with AsyncSqliteSaver.from_conn_string(str(DATABASE_PATH)) as saver:
#         await saver.setup()
#         _checkpointer = saver
#         try:
#             yield
#         finally:
#             _checkpointer = None


# def get_checkpointer() -> AsyncSqliteSaver:
#     """Return the active async SQLite checkpointer."""
#     if _checkpointer is None:
#         raise RuntimeError(
#             "Async checkpointer is not initialized. Attach `lifespan` to FastAPI."
#         )
#     return _checkpointer