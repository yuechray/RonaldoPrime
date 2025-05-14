from pydantic import  BaseModel, Field
from datetime import datetime
from typing import Optional

class ProductsModel(BaseModel):
    product_id: Optional[int] = None
    product_name: str = Field(max_length=255)
    manufacturer_id: int
    category_id: int
    date_price_change: datetime
    new_price: float
    is_available: bool = True

class ProductCreate(BaseModel):
    product_name: str = Field(max_length=255)
    manufacturer_id: int
    category_id: int
    new_price: float
    date_price_change: Optional[datetime] = None