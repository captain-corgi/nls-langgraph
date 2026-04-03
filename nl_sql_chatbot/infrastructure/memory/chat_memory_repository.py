from collections import defaultdict

from domain.entities.chat_message import ChatMessage
from domain.repositories.chat_repository import ChatRepository


class InMemoryChatRepository(ChatRepository):
    def __init__(self) -> None:
        self._store: dict[str, list[ChatMessage]] = defaultdict(list)

    def save_message(self, session_id: str, message: ChatMessage) -> None:
        self._store[session_id].append(message)

    def get_history(self, session_id: str) -> list[ChatMessage]:
        return list(self._store[session_id])

    def clear_session(self, session_id: str) -> None:
        self._store.pop(session_id, None)

    def list_sessions(self) -> list[str]:
        return list(self._store.keys())
