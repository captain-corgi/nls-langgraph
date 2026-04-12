from functools import lru_cache

from application.agents.sql_agent import SqlAgent
from infrastructure.settings import get_settings
from infrastructure.database.sql_database_adapter import SqlDatabaseAdapter
from infrastructure.memory.in_memory_chat_history import InMemoryChatHistory


@lru_cache
def get_db_repo() -> SqlDatabaseAdapter:
    settings = get_settings()
    return SqlDatabaseAdapter(
        database_url=settings.database_url,
        max_rows=settings.max_query_results,
    )


@lru_cache
def get_chat_repo() -> InMemoryChatHistory:
    return InMemoryChatHistory()


@lru_cache
def get_agent() -> SqlAgent:
    return SqlAgent(db_repo=get_db_repo(), chat_repo=get_chat_repo())
