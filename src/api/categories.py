from fastapi import APIRouter

from src.services.category import get_all_categories
from src.models.categories import CategoriesModel
from src.api.dependencies import SessionFactoryDependency

router = APIRouter(prefix="/categories", tags=["Категории"])

@router.get("/", response_model=list[CategoriesModel])
async def read_categories(session: SessionFactoryDependency):
    return await get_all_categories(session)
