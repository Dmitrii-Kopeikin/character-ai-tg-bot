from typing import List, TYPE_CHECKING

from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .conversation import Conversation


class User(BaseModel):
    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        index=True,
        nullable=False,
    )
    locale: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
        default="ru",
    )
    current_conversation_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("conversation.id"),
        nullable=True,
    )

    current_conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        primaryjoin="User.current_conversation_id == Conversation.id",
    )
    conversations: Mapped[List["Conversation"]] = relationship(
        "Conversation",
        back_populates="user",
        primaryjoin="User.id == Conversation.user_id",
    )
