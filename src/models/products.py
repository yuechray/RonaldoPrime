from pydantic import  BaseModel, Field
from datetime import datetime

class ProductsModel(BaseModel):
    product_id: int 
    product_name: str = Field(max_length=255)
    manufacturer_id: int
    category_id: int
    date_price_change: datetime
    new_price: float