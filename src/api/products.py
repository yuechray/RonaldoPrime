from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.services.products import (
    get_products_by_category,
    create_product,
    update_product,
    delete_product,
    get_product_by_id
)
from src.models.products import ProductsModel, ProductCreate
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

@router.post(
    "/",
    response_model=ProductsModel,
    summary="Создать новый товар"
)
async def create_new_product(
    product: ProductCreate,
    session: SessionFactoryDependency
):
    try:
        new_product = await create_product(session, product)
        return new_product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put(
    "/{product_id}",
    response_model=ProductsModel,
    summary="Обновить существующий товар"
)
async def update_existing_product(
    product_id: int,
    product: ProductCreate,
    session: SessionFactoryDependency
):
    try:
        updated_product = await update_product(session, product_id, product)
        return updated_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/{product_id}",
    summary="Удалить товар"
)
async def delete_existing_product(
    product_id: int,
    session: SessionFactoryDependency
):
    try:
        success = await delete_product(session, product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Товар не найден")
        return {"message": "Товар успешно удален"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/{product_id}",
    response_model=ProductsModel,
    summary="Получить информацию о товаре"
)
async def get_product(
    product_id: int,
    session: SessionFactoryDependency,
    include_unavailable: bool = True
):
    product = await get_product_by_id(session, product_id, include_unavailable)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product