from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select

from app.database import Database

from ..models import ConversationRequest
from .base_dal import Dal


class ConversationRequestDal(Dal):
    _cls = ConversationRequest

    def _prefetch(
        self,
        query: Select,
    ) -> Select:
        return query.options(joinedload(ConversationRequest.conversation))

    async def create(
        self,
        conversation_id: int,
        request_message: str,
        session: AsyncSession | None = None,
    ) -> ConversationRequest | None:
        kwargs = Dal._prepare_kwargs(
            conversation_id=conversation_id,
            request_message=request_message,
        )

        conversation_request = ConversationRequest(**kwargs)
        session.add(conversation_request)
        await session.flush()
        await session.refresh(conversation_request)

        return conversation_request

    async def get(
        self,
        id: int,
        prefetch: bool = False,
        prefetch_collections: bool = False,
        session: AsyncSession | None = None,
    ) -> ConversationRequest | None:
        query = self._prepare_select_query(
            id=id,
            prefetch=prefetch,
            prefetch_collections=prefetch_collections,
        )

        result = await session.execute(query)
        return result.unique().scalar()

    async def get_all(
        self,
        conversation_id: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
        session: AsyncSession | None = None,
    ) -> List[ConversationRequest]:
        query = self._prepare_select_query(
            conversation_id=conversation_id,
            limit=limit,
            offset=offset,
        )

        result = await session.execute(query)
        return result.unique().scalars().all()

    async def update_response(
        self,
        id: int,
        response_message: str,
        session: AsyncSession | None = None,
    ) -> ConversationRequest | None:
        conversation_request = await self.get(id=id, session=session)

        if not conversation_request:
            return None

        kwargs = self._prepare_kwargs(
            response_message=response_message,
        )

        for key, value in kwargs.items():
            setattr(conversation_request, key, value)

        await session.flush()

        return conversation_request


conversation_request_dal = ConversationRequestDal(Database().sessionmaker)
