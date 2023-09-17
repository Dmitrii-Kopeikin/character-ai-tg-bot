from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .conversation import Conversation


class Character(BaseModel):
    name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    greetings: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    image: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    prompt: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    conversations: Mapped[List["Conversation"]] = relationship(
        "Conversation",
        back_populates="character",
    )
