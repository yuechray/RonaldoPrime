from pydantic import  BaseModel
from datetime import datetime

class PurchasesModel(BaseModel):
    purchases_id: int 
    customer_id: int 
    store_id: int
    purchase_date: datetime