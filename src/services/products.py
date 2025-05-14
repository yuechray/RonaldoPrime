from typing import List, Optional
from sqlalchemy import select, and_
from datetime import datetime

from src.api.dependencies import SessionFactoryDependency
from src.db.tables import ProductsTable
from src.models.products import ProductsModel, ProductCreate


async def get_products_by_category(session_factory: SessionFactoryDependency, category_id: int) -> List[ProductsModel]:
    async with session_factory() as session:
        query = select(ProductsTable).where(
            and_(
                ProductsTable.category_id == category_id,
                ProductsTable.is_available == True  # Показываем только доступные товары
            )
        )
        result = await session.execute(query)
        products = result.scalars().all()
        return [
            ProductsModel.model_validate(prod, from_attributes=True)
            for prod in products
        ]

async def get_product_by_id(
    session_factory: SessionFactoryDependency,
    product_id: int,
    include_unavailable: bool = False
) -> Optional[ProductsModel]:
    async with session_factory() as session:
        query = select(ProductsTable).where(ProductsTable.product_id == product_id)
        if not include_unavailable:
            query = query.where(ProductsTable.is_available == True)
        result = await session.execute(query)
        product = result.scalar_one_or_none()
        if product:
            return ProductsModel.model_validate(product, from_attributes=True)
        return None

async def get_products_by_ids(session_factory: SessionFactoryDependency, product_ids: List[int]) -> List[ProductsModel]:
    async with session_factory() as session:
        query = select(ProductsTable).where(
            and_(
                ProductsTable.product_id.in_(product_ids),
                ProductsTable.is_available == True
            )
        )
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
            new_price=product.new_price,
            is_available=True
        )
        session.add(new_product)
        await session.commit()
        
        return ProductsModel.model_validate(new_product, from_attributes=True)

async def update_product(
    session_factory: SessionFactoryDependency,
    product_id: int,
    product_data: ProductCreate
) -> ProductsModel:
    async with session_factory() as session:
        query = select(ProductsTable).where(
            and_(
                ProductsTable.product_id == product_id,
                ProductsTable.is_available == True
            )
        )
        result = await session.execute(query)
        product = result.scalar_one_or_none()
        
        if not product:
            raise ValueError("Продукт не найден или недоступен")
        
        product.product_name = product_data.product_name
        product.manufacturer_id = product_data.manufacturer_id
        product.category_id = product_data.category_id
        product.date_price_change = product_data.date_price_change or datetime.now()
        product.new_price = product_data.new_price
        
        await session.commit()
        return ProductsModel.model_validate(product, from_attributes=True)

async def delete_product(
    session_factory: SessionFactoryDependency,
    product_id: int
) -> bool:
    async with session_factory() as session:
        query = select(ProductsTable).where(
            and_(
                ProductsTable.product_id == product_id,
                ProductsTable.is_available == True
            )
        )
        result = await session.execute(query)
        product = result.scalar_one_or_none()
        
        if not product:
            return False
        
        product.is_available = False  # Помечаем как недоступный вместо удаления
        await session.commit()
        return True

async def decrease_product_quantity(
    session_factory: SessionFactoryDependency,
    product_id: int,
    quantity: int = 1
) -> bool:
    async with session_factory() as session:
        query = select(ProductsTable).where(
            and_(
                ProductsTable.product_id == product_id,
                ProductsTable.is_available == True
            )
        )
        result = await session.execute(query)
        product = result.scalar_one_or_none()
        
        if not product:
            return False
            
        # Помечаем товар как недоступный вместо удаления
        product.is_available = False
        await session.commit()
        return True
