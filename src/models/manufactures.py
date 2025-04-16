from pydantic import  BaseModel, Field


class ManufacturersModel(BaseModel):
    manufacturer_id: int 
    manufacturer_name: str = Field(max_length=100)
