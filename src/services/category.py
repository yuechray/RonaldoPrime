from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.tables import CategoriesTable
from src.models.categories import CategoriesModel


async def get_all_categories(session: AsyncSession) -> List[CategoriesModel]:
    result = await session.execute(select(CategoriesTable))
    return [
        CategoriesModel.model_validate(category, from_attributes=True)
        for category in result.scalars()
    ]
