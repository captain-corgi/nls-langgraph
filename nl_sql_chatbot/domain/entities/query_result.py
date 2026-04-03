from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class QueryResult:
    sql: str
    data: list[dict[str, Any]]
    natural_answer: str
    row_count: int = 0
    execution_time_ms: float = 0.0
    error: str | None = None
    executed_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def success(self) -> bool:
        return self.error is None

    def to_dict(self) -> dict[str, Any]:
        return {
            "sql": self.sql,
            "data": self.data,
            "natural_answer": self.natural_answer,
            "row_count": self.row_count,
            "execution_time_ms": self.execution_time_ms,
            "error": self.error,
            "success": self.success,
            "executed_at": self.executed_at.isoformat(),
        }
