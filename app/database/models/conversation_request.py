from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .conversation import Conversation


class ConversationRequest(BaseModel):
    conversation_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("conversation.id"),
        nullable=False,
    )
    request_message: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    response_message: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="requests",
    )
