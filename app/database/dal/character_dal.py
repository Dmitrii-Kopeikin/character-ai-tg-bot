from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select

from app.database import Database

from ..models.character import Character
from .base_dal import Dal


class CharacterDal(Dal):
    _cls = Character

    def _prefetch_collections(
        self,
        query: Select,
    ) -> Select:
        return query.options(joinedload(Character.conversations))

    async def create(
        self,
        name: str,
        description: str,
        greetings: str,
        image: str,
        prompt: str,
        session: AsyncSession | None = None,
    ) -> Character:
        kwargs = Dal._prepare_kwargs(
            name=name,
            description=description,
            greetings=greetings,
            image=image,
            prompt=prompt,
        )

        character = Character(**kwargs)

        session.add(character)
        await session.flush()
        await session.refresh(character)

        return character

    async def get(
        self,
        id: int,
        prefetch: bool = False,
        prefetch_collections: bool = False,
        session: AsyncSession | None = None,
    ) -> Character | None:
        query = self._prepare_select_query(
            id=id,
            prefetch=prefetch,
            prefetch_collections=prefetch_collections,
        )

        result = await session.execute(query)
        return result.unique().scalar()

    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
        prefetch: bool = False,
        prefetch_collections: bool = False,
        session: AsyncSession | None = None,
    ) -> List[Character] | List[None]:
        query = self._prepare_select_query(
            limit=limit,
            offset=offset,
            prefetch=prefetch,
            prefetch_collections=prefetch_collections,
        )

        result = await session.execute(query)
        return result.unique().scalars().all()

    async def exists(
        self,
        id: int,
        session: AsyncSession | None = None,
    ):
        character = await self.get(id=id, session=session)

        return character is not None


character_dal = CharacterDal(Database().sessionmaker)
