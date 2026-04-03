import os

from config import get_settings


def configure_langsmith() -> None:
    settings = get_settings()
    os.environ["LANGCHAIN_TRACING_V2"] = settings.langchain_tracing_v2
    os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
    os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
    os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint

    if settings.langchain_tracing_v2.lower() == "true" and settings.langchain_api_key:
        print(
            f"[LangSmith] Tracing enabled — project: {settings.langchain_project}"
        )
    else:
        print("[LangSmith] Tracing disabled (no API key or tracing_v2 != true)")
