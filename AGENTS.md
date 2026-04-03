# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

NL→SQL Chatbot: a FastAPI + LangChain/LangGraph application that converts natural language questions to SQL queries. Clean Architecture with domain/application/infrastructure/interface layers. All source code lives under `nl_sql_chatbot/`.

### Running Commands

All commands must be run from `nl_sql_chatbot/` directory (the Python package root), not the workspace root.

- **Tests:** `python3 -m pytest tests/ -v`
- **Lint:** `python3 -m ruff check .`
- **Seed DB:** `python3 -m infrastructure.database.seed` (creates `data/sample.db`)
- **Start API:** `python3 -m uvicorn interface.api.main:app --host 0.0.0.0 --port 8000 --reload`
- **Health check:** `curl http://localhost:8000/chat/health`

### Key Gotchas

- The project uses Python module-style imports (e.g. `from config import get_settings`). The working directory must be `nl_sql_chatbot/` for imports to resolve.
- SQLite database file at `nl_sql_chatbot/data/sample.db` must exist before starting the API. Run `python3 -m infrastructure.database.seed` to create it.
- The `/chat/` and `/chat/stream` endpoints require a valid `OPENAI_API_KEY` environment variable or `.env` file entry. The `/chat/health` endpoint works without it.
- LangSmith tracing is optional. Set `LANGCHAIN_TRACING_V2=false` in `.env` to disable.
- `python` may not exist on the system; always use `python3`.
