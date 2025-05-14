from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PurchaseItemCreate(BaseModel):
    product_id: int
    product_name: str
    price: float

class PurchaseCreate(BaseModel):
    customer_id: int
    store_id: int
    products: List[PurchaseItemCreate]

class PurchaseItemModel(BaseModel):
    purchase_items_id: int
    purchases_id: int
    product_id: int
    product_count: int = 1 
    product_price: float

class PurchaseModel(BaseModel):
    purchase_id: int
    customer_id: int
    store_id: int
    purchase_date: datetime
    items: Optional[List[PurchaseItemModel]] = None 