from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .character import Character
    from .user import User
    from .conversation_request import ConversationRequest


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
    requests: Mapped["ConversationRequest"] = relationship(
        "ConversationRequest",
        back_populates="conversation",
    )
