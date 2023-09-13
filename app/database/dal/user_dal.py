from typing import List

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import Database

from ..models.user import User
from .base_dal import Dal


class UserDal(Dal):
    _cls = User

    def _prefetch(
        self,
        query: Select,
    ) -> Select:
        return query.options(joinedload(User.current_conversation))

    def _prefetch_collections(
        self,
        query: Select,
    ) -> Select:
        return query.options(joinedload(User.conversations))

    async def create(
        self,
        tg_id: int,
        locale: str | None = "ru",
        session: AsyncSession | None = None,
    ) -> User | None:
        kwargs = Dal._prepare_kwargs(tg_id=tg_id, locale=locale)

        user = User(**kwargs)

        session.add(user)
        await session.flush()
        await session.refresh(user)

        return user

    async def get(
        self,
        id: int | None = None,
        tg_id: int | None = None,
        session: AsyncSession | None = None,
        prefetch: bool = False,
        prefetch_collections: bool = False,
    ) -> User | None:
        query = self._prepare_select_query(
            prefetch=prefetch,
            prefetch_collections=prefetch_collections,
            id=id,
            tg_id=tg_id,
        )

        result = await session.execute(query)
        return result.unique().scalar()

    async def get_all(
        self,
        tg_id: int | None = None,
        locale: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        prefetch: bool = False,
        prefetch_collections: bool = False,
        session: AsyncSession | None = None,
    ) -> List[User]:
        query = self._prepare_select_query(
            prefetch=prefetch,
            prefetch_collections=prefetch_collections,
            limit=limit,
            offset=offset,
            tg_id=tg_id,
            locale=locale,
        )

        result = await session.execute(query)
        return result.unique().scalars().all()

    async def update(
        self,
        id: int,
        current_conversation_id: int | None = None,
        locale: str | None = None,
        session: AsyncSession | None = None,
    ) -> User | None:
        user = await self.get(id=id, session=session)

        if not user:
            return None

        kwargs = Dal._prepare_kwargs(
            current_conversation_id=current_conversation_id,
            locale=locale,
        )

        for key, value in kwargs.items():
            setattr(user, key, value)

        await session.flush()

        return user

    async def exists(
        self,
        id: int | None = None,
        tg_id: int | None = None,
        session: AsyncSession | None = None,
    ):
        user = await self.get(
            id=id,
            tg_id=tg_id,
            session=session,
        )
        return user is not None


user_dal = UserDal(Database().sessionmaker)
