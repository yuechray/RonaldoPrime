from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt
from src.models.customers import CustomersModel

async def authenticate_user(email: str, password: str, session: AsyncSession):
    query = select(CustomersModel).where(CustomersModel.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        return None

    if not bcrypt.verify(password, user.password_hash):
        return None

    return user


