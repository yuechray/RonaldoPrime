from pydantic import  BaseModel, Field


class PurchaseItemsModel(BaseModel):
    purchase_items_id: int 
    purchases_id: int 
    product_id: int
    product_count: int
    product_price: float