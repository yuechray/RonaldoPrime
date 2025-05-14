from typing import List
from sqlalchemy import select

from src.api.dependencies import SessionFactoryDependency
from src.db.tables import ManufacturersTable
from src.models.manufactures import ManufacturersModel

async def get_all_manufacturers(session_factory: SessionFactoryDependency) -> List[ManufacturersModel]:
    async with session_factory() as session:
        result = await session.execute(select(ManufacturersTable))
        return [
            ManufacturersModel.model_validate(manufacturer, from_attributes=True)
            for manufacturer in result.scalars()
        ] 