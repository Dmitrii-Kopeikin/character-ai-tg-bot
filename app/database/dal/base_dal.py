from functools import wraps
from inspect import isfunction
from typing import Any, Dict, Union, Callable, Self

from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..models.base_model import BaseModel

from abc import ABC


class Dal(ABC):
    sessionmaker: async_sessionmaker
    _cls: BaseModel

    def __new__(cls, *args, **kwargs):
        for k, v in cls.__dict__.items():
            if not isfunction(v):
                continue
            for _, t in v.__annotations__.items():
                if t == Union[AsyncSession, None]:
                    setattr(cls, k, cls.get_asyncsession_if_not_passed(cls, v))

        return super().__new__(cls)

    def __init__(
        self: Self,
        sessionmaker: async_sessionmaker,
    ) -> None:
        self.sessionmaker = sessionmaker

    def _prepare_select_query(
        self: Self,
        prefetch: bool = False,
        prefetch_collections: bool = False,
        limit: int | None = None,
        offset: int | None = None,
        **kwargs,
    ) -> Select:
        query = select(self._cls)

        query = Dal._prepare_where_clause(
            query=query,
            cls=self._cls,
            **kwargs,
        )

        if prefetch:
            query = self._prefetch(query)

        if prefetch_collections:
            query = self._prefetch_collections(query)

        if limit or offset:
            query = self._add_limit_offset(
                query=query,
                limit=limit,
                offset=offset,
            )

        return query

    # @staticmethod
    def get_asyncsession_if_not_passed(
        self: Self,
        func: Callable[[Any], Any],
    ) -> Callable[[Any], Any]:
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            session: AsyncSession | None = None
            for arg in args:
                if isinstance(arg, AsyncSession):
                    session = arg
            for key, value in kwargs.items():
                if key == "session" and isinstance(value, AsyncSession):
                    session = value

            try:
                if session:
                    return await func(self, *args, **kwargs)

                async with self.sessionmaker() as session:
                    kwargs["session"] = session
                    result = await func(
                        self,
                        *args,
                        **kwargs,
                    )
                    await session.commit()
                    return result
            except SQLAlchemyError as error:
                # TODO: Log error.
                print(error)

            return None

        return wrapper

    @staticmethod
    def _prepare_where_clause(query: Select, cls: type, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                query = query.where(getattr(cls, key) == value)

        return query

    @staticmethod
    def _add_limit_offset(
        query: Select,
        limit: int | None = 0,
        offset: int | None = 0,
    ) -> Select:
        if not offset:
            offset = 0
        if not limit:
            limit = 0

        if offset > 0:
            query = query.offset(offset)
        if limit > 0:
            query = query.limit(limit)

        return query

    @staticmethod
    def _prepare_kwargs(**kwargs) -> Dict[str, Any]:
        return {k: v for k, v in kwargs.items() if v is not None}

    # @abstractmethod
    async def create():
        raise NotImplementedError()

    # @abstractmethod
    async def get():
        raise NotImplementedError()

    # @abstractmethod
    async def get_all():
        raise NotImplementedError()

    # @abstractmethod
    async def update():
        raise NotImplementedError()

    # @abstractmethod
    async def exists():
        raise NotImplementedError()

    # @abstractmethod
    def _prefetch(
        self,
        query: Select,
    ) -> Select:
        return query

    # @abstractmethod
    def _prefetch_collections(
        self,
        query: Select,
    ) -> Select:
        return query
