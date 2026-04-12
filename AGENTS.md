# AGENTS.md

## Cursor Cloud specific instructions

### Project Overview

NL→SQL Chatbot: a FastAPI + LangChain/LangGraph application that converts natural language questions to SQL queries. Clean Architecture with domain/application/infrastructure/interface layers. All source code lives under `nl_sql_chatbot/`.

### Running Commands

- **Tests** (from the **workspace root**): `python3 -m pytest tests/ -v` — `pyproject.toml` sets `pythonpath` to `nl_sql_chatbot/`.
- **Lint** (from the **workspace root**): `python3 -m ruff check nl_sql_chatbot`
- **Seed DB** (from `nl_sql_chatbot/`): `python3 -m infrastructure.database.seed` (creates `data/sample.db`)
- **Start API** (from `nl_sql_chatbot/`): `python3 -m uvicorn interface.api.main:app --host 0.0.0.0 --port 8000 --reload`
- **Health check:** `curl http://localhost:8000/chat/health`

### Key Gotchas

- The project uses Python module-style imports (e.g. `from infrastructure.settings import get_settings`). The working directory must be `nl_sql_chatbot/` for the API, CLI, and seed commands so those imports resolve.
- SQLite database file at `nl_sql_chatbot/data/sample.db` must exist before starting the API. Run `python3 -m infrastructure.database.seed` to create it.
- The `/chat/` and `/chat/stream` endpoints require a valid `OPENAI_API_KEY` environment variable or `.env` file entry. The `/chat/health` endpoint works without it.
- LangSmith tracing is optional. Set `LANGCHAIN_TRACING_V2=false` in `.env` to disable.
- `python` may not exist on the system; always use `python3`.

## Learned User Preferences

- When asked to babysit or unblock a PR, poll GitHub checks and review threads until the latest push is fully green and feedback is addressed, not only a single snapshot in time.

## Learned Workspace Facts

- GitHub Actions (`.github/workflows/ci.yml`) runs on pull requests and on pushes to `DevMaster` and `main`: Python 3.12, `pip install -r nl_sql_chatbot/requirements.txt ruff`, then `ruff check nl_sql_chatbot` and `pytest tests/` from the repo root.
- `ruff` is not declared in `nl_sql_chatbot/requirements.txt`; CI installs it explicitly. For local lint, install `ruff` in the active environment if `python3 -m ruff` fails with “No module named ruff”.
- Outbound boundaries use port/adapter naming: `domain/ports/sql_database_port.py` (`SqlDatabasePort`), `domain/ports/chat_history_port.py` (`ChatHistoryPort`), with `SqlDatabaseAdapter` and `InMemoryChatHistory` in infrastructure (avoid legacy `domain/repositories/` and `*Repository` types when editing this codebase).
