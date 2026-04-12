from typing import Any

import sqlalchemy
from langchain_community.utilities import SQLDatabase

from domain.ports.sql_database_port import SqlDatabasePort


class SqlDatabaseAdapter(SqlDatabasePort):
    def __init__(self, database_url: str, max_rows: int = 100):
        self._database_url = database_url
        self._max_rows = max_rows
        self._db = SQLDatabase.from_uri(database_url, sample_rows_in_table_info=3)

    def get_table_names(self) -> list[str]:
        return self._db.get_usable_table_names()

    def get_table_schema(self, table_name: str) -> str:
        return self._db.get_table_info(table_names=[table_name])

    def get_all_schemas(self) -> str:
        return self._db.get_table_info()

    def execute_query(self, sql: str) -> list[dict[str, Any]]:
        engine = self._db._engine
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(sql))
            rows = result.fetchmany(self._max_rows)
            columns = list(result.keys())
        return [dict(zip(columns, row)) for row in rows]

    def get_sample_rows(self, table_name: str, n: int = 3) -> list[dict[str, Any]]:
        return self.execute_query(f"SELECT * FROM {table_name} LIMIT {n}")

    def get_langchain_db(self) -> SQLDatabase:
        return self._db
