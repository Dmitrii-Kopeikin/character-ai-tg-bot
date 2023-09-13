from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database import Database

database = Database()


async def get_sessionmaker() -> async_sessionmaker:
    return database.sessionmaker


async def get_session() -> AsyncSession:
    async with database.sessionmaker() as session:
        yield session
