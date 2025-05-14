from typing import List
from sqlalchemy import select
from datetime import datetime

from src.api.dependencies import SessionFactoryDependency
from src.db.tables import ProductsTable
from src.models.products import ProductsModel, ProductCreate


async def get_products_by_category(session_factory: SessionFactoryDependency, category_id: int) -> List[ProductsModel]:
    async with session_factory() as session:
        query = select(ProductsTable).where(ProductsTable.category_id == category_id)
        result = await session.execute(query)
        products = result.scalars().all()
        return [
            ProductsModel.model_validate(prod, from_attributes=True)
            for prod in products
        ]

async def get_products_by_ids(session_factory: SessionFactoryDependency, product_ids: List[int]) -> List[ProductsModel]:
    async with session_factory() as session:
        query = select(ProductsTable).where(ProductsTable.product_id.in_(product_ids))
        result = await session.execute(query)
        products = result.scalars().all()
        return [ProductsModel.model_validate(product) for product in products]

async def create_product(
    session_factory: SessionFactoryDependency,
    product: ProductCreate
) -> ProductsModel:
    async with session_factory() as session:
        new_product = ProductsTable(
            product_name=product.product_name,
            manufacturer_id=product.manufacturer_id,
            category_id=product.category_id,
            date_price_change=product.date_price_change or datetime.now(),
            new_price=product.new_price
        )
        session.add(new_product)
        await session.commit()
        
        return ProductsModel.model_validate(new_product, from_attributes=True)
