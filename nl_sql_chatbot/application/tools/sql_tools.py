from langchain_core.tools import BaseTool
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)

from infrastructure.ai.llm_provider import create_llm
from infrastructure.database.sql_database_repository import SqlDatabaseRepository


def build_sql_tools(db_repo: SqlDatabaseRepository) -> list[BaseTool]:
    db = db_repo.get_langchain_db()
    return [
        ListSQLDatabaseTool(db=db),
        InfoSQLDatabaseTool(db=db),
        QuerySQLDataBaseTool(db=db),
        QuerySQLCheckerTool(db=db, llm=create_llm()),
    ]
