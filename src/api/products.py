from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.services.products import get_products_by_category
from src.models.products import ProductsModel
from src.api.dependencies import SessionFactoryDependency

router = APIRouter(prefix="/products", tags=["Товары"])

@router.get(
    "/by-category/{category_id}",
    response_model=List[ProductsModel],
    summary="Получить товары заданной категории"
)
async def read_products_by_category(
    category_id: int,
    session: SessionFactoryDependency
):
    products = await get_products_by_category(session, category_id)
    if not products:
        
        raise HTTPException(status_code=404, detail="Товары не найдены")
    return products