from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .character import Character
    from .conversation_request import ConversationRequest
    from .user import User


class Conversation(BaseModel):
    character_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("character.id")
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id"),
    )

    character: Mapped["Character"] = relationship(
        "Character",
        back_populates="conversations",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="conversations",
        foreign_keys="Conversation.user_id",
    )
    requests: Mapped[List["ConversationRequest"]] = relationship(
        "ConversationRequest",
        back_populates="conversation",
    )
