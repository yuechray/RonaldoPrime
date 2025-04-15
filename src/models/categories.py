from pydantic import  BaseModel, Field


class CategoriesModel(BaseModel):
    category_id: int = Field(ge=0)
    category_name: str = Field(max_length=100)
