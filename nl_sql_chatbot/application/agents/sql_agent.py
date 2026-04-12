from typing import Generator

from langchain_core.messages import AIMessage, HumanMessage

from application.agents.graph_builder import build_graph
from application.tools.sql_tools import build_sql_tools
from domain.entities.chat_message import ChatMessage, MessageRole
from domain.ports.chat_history_port import ChatHistoryPort
from infrastructure.ai.llm_provider import create_llm
from infrastructure.database.sql_database_adapter import SqlDatabaseAdapter


class SqlAgent:
    def __init__(
        self, db_repo: SqlDatabaseAdapter, chat_repo: ChatHistoryPort
    ) -> None:
        self._db_repo = db_repo
        self._chat_repo = chat_repo
        llm = create_llm()
        tools = build_sql_tools(db_repo)
        table_info = db_repo.get_all_schemas()
        self._graph = build_graph(llm, tools, table_info)

    def _history_to_lc_messages(
        self, history: list[ChatMessage]
    ) -> list[HumanMessage | AIMessage]:
        messages: list[HumanMessage | AIMessage] = []
        for msg in history:
            if msg.role == MessageRole.USER:
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == MessageRole.ASSISTANT:
                messages.append(AIMessage(content=msg.content))
        return messages

    def chat(self, session_id: str, user_input: str) -> str:
        self._chat_repo.save_message(session_id, ChatMessage.user(user_input))
        history = self._chat_repo.get_history(session_id)
        lc_messages = self._history_to_lc_messages(history)
        result = self._graph.invoke(
            {"messages": lc_messages, "session_id": session_id}
        )
        answer = result["messages"][-1].content
        self._chat_repo.save_message(session_id, ChatMessage.assistant(answer))
        return answer

    def stream_chat(
        self, session_id: str, user_input: str
    ) -> Generator[str, None, None]:
        self._chat_repo.save_message(session_id, ChatMessage.user(user_input))
        history = self._chat_repo.get_history(session_id)
        lc_messages = self._history_to_lc_messages(history)
        full_answer = ""
        for state in self._graph.stream(
            {"messages": lc_messages, "session_id": session_id},
            stream_mode="values",
        ):
            messages = state.get("messages", [])
            if messages:
                last = messages[-1]
                if isinstance(last, AIMessage) and last.content:
                    delta = last.content[len(full_answer) :]
                    if delta:
                        full_answer = last.content
                        yield delta
        if full_answer:
            self._chat_repo.save_message(
                session_id, ChatMessage.assistant(full_answer)
            )

    def clear_session(self, session_id: str) -> None:
        self._chat_repo.clear_session(session_id)
