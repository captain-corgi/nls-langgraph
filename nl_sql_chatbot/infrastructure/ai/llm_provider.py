from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

from infrastructure.settings import get_settings


def create_llm(
    *, model: str | None = None, temperature: float = 0.0, streaming: bool = False
) -> BaseChatModel:
    settings = get_settings()
    return ChatOpenAI(
        model=model or settings.openai_model,
        temperature=temperature,
        streaming=streaming,
        api_key=settings.openai_api_key,
    )
