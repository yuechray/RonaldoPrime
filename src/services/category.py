from typing import List

from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession
from sqlalchemy.future import select

from src.db.tables import CategoriesTable
from src.models.categories import CategoriesModel


async def get_all_categories(session_factory: async_sessionmaker[AsyncSession]) -> List[CategoriesModel]:
    async with session_factory() as session:
        result = await session.execute(select(CategoriesTable))
    return [
        CategoriesModel.model_validate(category, from_attributes=True)
        for category in result.scalars()
    ]
