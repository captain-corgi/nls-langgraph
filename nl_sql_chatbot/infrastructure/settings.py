from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    langchain_tracing_v2: str = "false"
    langchain_api_key: str = ""
    langchain_project: str = "nl-sql-chatbot"
    langchain_endpoint: str = "https://api.smith.langchain.com"
    database_url: str = "sqlite:///./data/sample.db"
    app_env: str = "development"
    app_debug: bool = True
    max_query_results: int = 100
    agent_max_iterations: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()
