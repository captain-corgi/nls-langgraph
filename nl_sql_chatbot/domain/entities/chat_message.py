from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


@dataclass
class ChatMessage:
    content: str
    role: MessageRole
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "role": self.role.value,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def user(cls, content: str, **metadata: Any) -> "ChatMessage":
        return cls(content=content, role=MessageRole.USER, metadata=metadata)

    @classmethod
    def assistant(cls, content: str, **metadata: Any) -> "ChatMessage":
        return cls(content=content, role=MessageRole.ASSISTANT, metadata=metadata)
