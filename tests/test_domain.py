from datetime import datetime
from uuid import UUID

from domain.entities.chat_message import ChatMessage, MessageRole
from domain.entities.query_result import QueryResult
from infrastructure.memory.chat_memory_repository import InMemoryChatRepository


class TestChatMessage:
    def test_user_factory(self):
        msg = ChatMessage.user("Hello")
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello"
        assert isinstance(msg.id, UUID)
        assert isinstance(msg.created_at, datetime)

    def test_assistant_factory(self):
        msg = ChatMessage.assistant("Hi there")
        assert msg.role == MessageRole.ASSISTANT
        assert msg.content == "Hi there"

    def test_to_dict(self):
        msg = ChatMessage.user("test")
        d = msg.to_dict()
        assert "role" in d
        assert "content" in d
        assert "id" in d
        assert "created_at" in d


class TestQueryResult:
    def test_success_property(self):
        qr = QueryResult(sql="SELECT 1", data=[], natural_answer="One", error=None)
        assert qr.success is True

    def test_failure_property(self):
        qr = QueryResult(
            sql="SELECT bad", data=[], natural_answer="", error="syntax error"
        )
        assert qr.success is False

    def test_to_dict(self):
        qr = QueryResult(sql="SELECT 1", data=[], natural_answer="One")
        d = qr.to_dict()
        assert "sql" in d
        assert "success" in d


class TestInMemoryChatRepository:
    def test_save_and_retrieve(self):
        repo = InMemoryChatRepository()
        msg1 = ChatMessage.user("Hello")
        msg2 = ChatMessage.assistant("Hi")
        repo.save_message("s1", msg1)
        repo.save_message("s1", msg2)
        history = repo.get_history("s1")
        assert len(history) == 2
        assert history[0].content == "Hello"
        assert history[1].content == "Hi"

    def test_sessions_are_isolated(self):
        repo = InMemoryChatRepository()
        repo.save_message("a", ChatMessage.user("A"))
        repo.save_message("b", ChatMessage.user("B"))
        assert len(repo.get_history("a")) == 1
        assert len(repo.get_history("b")) == 1
        assert repo.get_history("a")[0].content == "A"
        assert repo.get_history("b")[0].content == "B"

    def test_clear_session(self):
        repo = InMemoryChatRepository()
        repo.save_message("s1", ChatMessage.user("Hello"))
        repo.clear_session("s1")
        assert repo.get_history("s1") == []
