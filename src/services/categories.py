from sqlalchemy import select, update as sql_update, delete as sql_delete
from src.db.tables import CategoriesTable
from src.api.dependencies import SessionFactoryDependency

class CategoriesRepository:
    def __init__(self, session_factory: SessionFactoryDependency):
        self.session_factory = session_factory

    async def create(self, category_name: str) -> CategoriesTable:
        async with self.session_factory() as session:
            new_category = CategoriesTable(category_name=category_name)
            session.add(new_category)
            await session.commit()
            await session.refresh(new_category)
            return new_category

    async def get_all(self) -> list[CategoriesTable]:
        async with self.session_factory() as session:
            result = await session.execute(select(CategoriesTable))
            return result.scalars().all()

    async def get_by_id(self, category_id: int) -> CategoriesTable | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(CategoriesTable).where(CategoriesTable.category_id == category_id)
            )
            return result.scalar_one_or_none()

    async def get_by_name(self, category_name: str) -> list[CategoriesTable]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(CategoriesTable).where(CategoriesTable.category_name.ilike(f"%{category_name}%"))
            )
            return result.scalars().all()

    async def update(self, category_id: int, new_name: str) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(
                sql_update(CategoriesTable)
                .where(CategoriesTable.category_id == category_id)
                .values(category_name=new_name)
                .execution_options(synchronize_session="fetch")
            )
            await session.commit()
            return result.rowcount > 0

    async def delete(self, category_id: int) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(
                sql_delete(CategoriesTable)
                .where(CategoriesTable.category_id == category_id)
            )
            await session.commit()
            return result.rowcount > 0