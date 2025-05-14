from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.api.dependencies import SessionFactoryDependency
from src.db.tables import ProductsTable
from src.models.products import ProductsModel


async def get_products_by_category(session_factory: SessionFactoryDependency, category_id :int) -> List[ProductsModel]:
    async with session_factory() as session:
        result = await session.execute(
            select(ProductsTable)
            .where(ProductsTable.category_id == category_id)
        )
        products = result.scalars().all()
    return [
        ProductsModel.model_validate(prod, from_attributes=True)
        for prod in products
    ]
