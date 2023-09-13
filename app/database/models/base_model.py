from datetime import datetime

from sqlalchemy import DateTime, BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column

from app.utils.camel_to_snake import camel_to_snake
from sqlalchemy import func


@as_declarative()
class BaseModel(AsyncAttrs):
    __name__: str

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
    )
    modified_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)
