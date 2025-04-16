from functools import lru_cache
from src.api.dependencies import SettingsDependency

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Postgres:
    def __init__(self, *, postgres_dsn: str) -> None:
        self.engine: AsyncEngine = create_async_engine(postgres_dsn)
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )


@lru_cache(maxsize=4, typed=True)
def get_postgres_manager(postgres_dsn: str):
    return Postgres(postgres_dsn=postgres_dsn)


async def get_async_session_factory(
        settings: SettingsDependency
) -> async_sessionmaker[AsyncSession]:
    postgres = get_postgres_manager(settings.postgres_dsn)

    return postgres.session_factory