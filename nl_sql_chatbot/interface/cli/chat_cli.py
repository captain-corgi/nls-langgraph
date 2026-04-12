import sys
import uuid

from application.agents.sql_agent import SqlAgent
from infrastructure.settings import get_settings
from infrastructure.ai.langsmith_config import configure_langsmith
from infrastructure.database.sql_database_adapter import SqlDatabaseAdapter
from infrastructure.memory.in_memory_chat_history import InMemoryChatHistory


def run() -> None:
    configure_langsmith()
    settings = get_settings()

    db_repo = SqlDatabaseAdapter(
        database_url=settings.database_url,
        max_rows=settings.max_query_results,
    )
    chat_repo = InMemoryChatHistory()
    agent = SqlAgent(db_repo=db_repo, chat_repo=chat_repo)

    session_id = str(uuid.uuid4())

    print("=" * 60)
    print("  NL→SQL Chatbot  |  Interactive REPL")
    print("=" * 60)
    print(f"  Database: {settings.database_url}")
    print(f"  Tables:   {', '.join(db_repo.get_table_names())}")
    print(f"  Session:  {session_id}")
    print("-" * 60)
    print("  Commands: quit/exit/q, clear")
    print("=" * 60)

    try:
        while True:
            try:
                user_input = input("\n[You] > ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break

            if user_input.lower() == "clear":
                agent.clear_session(session_id)
                session_id = str(uuid.uuid4())
                print(f"[System] Session cleared. New session: {session_id}")
                continue

            print("\n[Assistant] ", end="", flush=True)
            for chunk in agent.stream_chat(session_id, user_input):
                print(chunk, end="", flush=True)
            print()

    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    run()
