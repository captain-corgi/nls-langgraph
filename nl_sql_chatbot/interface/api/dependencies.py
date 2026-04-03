from functools import lru_cache

from application.agents.sql_agent import SqlAgent
from config import get_settings
from infrastructure.database.sql_database_repository import SqlDatabaseRepository
from infrastructure.memory.chat_memory_repository import InMemoryChatRepository


@lru_cache
def get_db_repo() -> SqlDatabaseRepository:
    settings = get_settings()
    return SqlDatabaseRepository(
        database_url=settings.database_url,
        max_rows=settings.max_query_results,
    )


@lru_cache
def get_chat_repo() -> InMemoryChatRepository:
    return InMemoryChatRepository()


@lru_cache
def get_agent() -> SqlAgent:
    return SqlAgent(db_repo=get_db_repo(), chat_repo=get_chat_repo())
