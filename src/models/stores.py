from pydantic import  BaseModel, Field


class StoresModel(BaseModel):
    store_id: int 
    store_name: str = Field(max_length=255)