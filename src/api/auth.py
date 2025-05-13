from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth import LoginRequest
from src.services.auth import authenticate_user
from src.api.dependencies import SessionFactoryDependency

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(
    data: LoginRequest,
    session_factory: SessionFactoryDependency,
):
    async with session_factory() as session:
        user = await authenticate_user(data.email, data.password, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )
        return {"message": "Успешный вход", "user_id": user.customer_id}