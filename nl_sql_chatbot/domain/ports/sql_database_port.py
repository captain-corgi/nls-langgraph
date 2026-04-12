from abc import ABC, abstractmethod
from typing import Any


class SqlDatabasePort(ABC):
    @abstractmethod
    def get_table_names(self) -> list[str]: ...

    @abstractmethod
    def get_table_schema(self, table_name: str) -> str: ...

    @abstractmethod
    def get_all_schemas(self) -> str: ...

    @abstractmethod
    def execute_query(self, sql: str) -> list[dict[str, Any]]: ...

    @abstractmethod
    def get_sample_rows(self, table_name: str, n: int = 3) -> list[dict[str, Any]]: ...
