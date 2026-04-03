from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.ai.langsmith_config import configure_langsmith
from interface.api.routes.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_langsmith()
    print("[API] NL→SQL Chatbot is ready!")
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="NL→SQL Chatbot",
        description="Natural Language to SQL chatbot powered by LangChain + LangGraph",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(chat_router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("interface.api.main:app", host="0.0.0.0", port=8000, reload=True)
