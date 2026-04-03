from abc import ABC, abstractmethod

from domain.entities.chat_message import ChatMessage


class ChatRepository(ABC):
    @abstractmethod
    def save_message(self, session_id: str, message: ChatMessage) -> None: ...

    @abstractmethod
    def get_history(self, session_id: str) -> list[ChatMessage]: ...

    @abstractmethod
    def clear_session(self, session_id: str) -> None: ...
