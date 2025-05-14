from fastapi import APIRouter, Depends, HTTPException
from typing import List


from src.api.dependencies import SessionFactoryDependency
from src.services.purchases import create_purchase, get_user_purchases
from src.models.purchases import PurchaseCreate, PurchaseModel

router = APIRouter(prefix="/purchases", tags=["Покупки"])

@router.post("/", response_model=PurchaseModel)
async def make_purchase(
    purchase: PurchaseCreate,
    session: SessionFactoryDependency
):
    try:
        new_purchase = await create_purchase(session, purchase)
        return new_purchase
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=List[PurchaseModel])
async def get_purchases(
    user_id: int,
    session: SessionFactoryDependency
):
    purchases = await get_user_purchases(session, user_id)
    return purchases 