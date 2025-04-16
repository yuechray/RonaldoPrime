from pydantic import  BaseModel
from datetime import datetime

class DeliveriesModel(BaseModel):
    deliveries_id: int 
    product_id: int 
    store_id: int
    deliveries_date: datetime
    product_count: int 