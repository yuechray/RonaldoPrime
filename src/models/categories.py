from pydantic import  BaseModel, Field


class CategoriesModel(BaseModel):
    category_id: int 
    category_name: str = Field(max_length=100)
