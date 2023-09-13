from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy_utils.functions import create_database, database_exists

from config import config
from app.utils.singleton_meta import SingletonMeta

from .models.base_model import BaseModel

import logging

logger = logging.getLogger("Database")


class Database(metaclass=SingletonMeta):
    """
    Represents a singleton database instance.

    Methods:
        __init__(): Initializes the Database class.
        init_database(): Initializes the database connection.

    """

    def __init__(self):
        """
        Initializes the Database class.

        Attributes:
            engine: The SQLAlchemy create_async_engine with a PostgreSQL URL.
            sessionmaker: The asynchronous sessionmaker.

        """
        self.engine = create_async_engine(config.postgres.inner_url)
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def init_database(self) -> None:
        """
        Initializes the database.

        Checks if the sync connection URL exists and creates the database
        if it doesn't.
        Then, creates all the tables defined in the Base.metadata.

        """
        sync_conn_url = config.postgres.sync_inner_url
        if not database_exists(sync_conn_url):
            logger.info(
                f"Database {config.postgres.db} doesn't exist."
                "Creating database..."
            )
            create_database(sync_conn_url)

        async with self.engine.begin() as connection:
            await connection.run_sync(BaseModel.metadata.create_all)

    async def close(self):
        await self.engine.dispose()
