from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.core.settings import Settings, get_app_settings
from src.db.postgres import get_postgres_manager
from src.db.postgres import get_async_session_factory


SettingsDependency = Annotated[Settings, Depends(get_app_settings)]
SessionFactoryDependency = Annotated[
    async_sessionmaker[AsyncSession],
    Depends(get_async_session_factory)
]
