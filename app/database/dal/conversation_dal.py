from typing import List

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import Database

from ..models.conversation import Conversation
from .base_dal import Dal


class ConversationDal(Dal):
    def _prefetch(
        self,
        query: Select,
    ) -> Select:
        return query.options(
            joinedload(Conversation.user),
            joinedload(Conversation.character),
        )

    def _prefetch_collections(
        self,
        query: Select,
    ) -> Select:
        return query.options(joinedload(Conversation.requests))

    async def create(
        self,
        character_id: int,
        user_id: int,
        session: AsyncSession | None = None,
    ) -> Conversation | None:
        kwargs = Dal._prepare_kwargs(
            character_id=character_id,
            user_id=user_id,
        )

        conversation = Conversation(**kwargs)

        session.add(conversation)
        await session.flush()
        await session.refresh(conversation)

        return conversation

    async def get(
        self,
        id: int,
        prefetch: bool = False,
        prefetch_collections: bool = False,
        session: AsyncSession | None = None,
    ) -> List[Conversation]:
        query = self._prepare_select_query(
            id=id,
            prefetch=prefetch,
            prefetch_collections=prefetch_collections,
        )

        result = await session.execute(query)
        return result.unique().scalars()


conversation_dal = ConversationDal(Database().sessionmaker)
