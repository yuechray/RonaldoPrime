from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt
from sqlalchemy.future import select
from sqlalchemy import text
from src.models.auth import LoginRequest
from src.api.dependencies import SessionFactoryDependency
from src.db.tables import CustomersTable


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(
    data: LoginRequest,
    session_factory: SessionFactoryDependency
):
    email = data.email

    async with session_factory() as session:
        
        result = await session.execute(
            select(CustomersTable).filter_by(email=email)
        )
        user = result.scalars().first()  
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")

        
        if not bcrypt.verify(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        return {
            "message": "Успешная авторизация",
            "user_id": user.customer_id,
            "name": user.customer_fname
        }
    
