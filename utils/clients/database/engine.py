from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import settings
from utils.clients.database.base_model import Base


async def get_database_engine() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(settings.database_url, echo=True, future=True)
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_database():
    engine = create_async_engine(settings.database_url, echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
