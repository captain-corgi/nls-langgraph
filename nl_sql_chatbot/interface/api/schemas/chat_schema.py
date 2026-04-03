from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    message_count: int | None = None


class ClearSessionRequest(BaseModel):
    session_id: str


class HealthResponse(BaseModel):
    status: str = "ok"
    tables: list[str] = []
