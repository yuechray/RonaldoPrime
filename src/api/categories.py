from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.services.category import get_all_categories
from src.models.categories import CategoriesModel
from src.api.dependencies import SessionFactoryDependency

router = APIRouter(prefix="/categories", tags=["Категории"])

@router.get("/", response_model=List[CategoriesModel])
async def read_categories(session: AsyncSession = Depends(SessionFactoryDependency)):
    return await get_all_categories(session)