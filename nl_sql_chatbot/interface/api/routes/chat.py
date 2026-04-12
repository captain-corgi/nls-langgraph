from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from application.agents.sql_agent import SqlAgent
from infrastructure.database.sql_database_adapter import SqlDatabaseAdapter
from interface.api.dependencies import get_agent, get_db_repo
from interface.api.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    ClearSessionRequest,
    HealthResponse,
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/health", response_model=HealthResponse)
def health(db_repo: SqlDatabaseAdapter = Depends(get_db_repo)) -> HealthResponse:
    try:
        tables = db_repo.get_table_names()
        return HealthResponse(status="ok", tables=tables)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, agent: SqlAgent = Depends(get_agent)) -> ChatResponse:
    try:
        answer = agent.chat(request.session_id, request.message)
        return ChatResponse(
            session_id=request.session_id,
            answer=answer,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
def stream_chat(
    request: ChatRequest, agent: SqlAgent = Depends(get_agent)
) -> StreamingResponse:
    def event_generator():
        try:
            for chunk in agent.stream_chat(request.session_id, request.message):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: ERROR: {e}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.delete("/session")
def clear_session(
    request: ClearSessionRequest, agent: SqlAgent = Depends(get_agent)
) -> dict:
    try:
        agent.clear_session(request.session_id)
        return {"message": f"Session '{request.session_id}' cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
