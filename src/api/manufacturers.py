from fastapi import APIRouter

from src.services.manufacturers import get_all_manufacturers
from src.models.manufactures import ManufacturersModel
from src.api.dependencies import SessionFactoryDependency

router = APIRouter(prefix="/manufacturers", tags=["Производители"])

@router.get("/", response_model=list[ManufacturersModel])
async def read_manufacturers(session: SessionFactoryDependency):
    return await get_all_manufacturers(session) 