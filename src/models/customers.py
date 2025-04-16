from pydantic import  BaseModel, Field, EmailStr


class CustomersModel(BaseModel):
    customer_id: int 
    customer_fname: str = Field(max_length=100)
    customer_lname: str = Field(max_length=100)
    email: EmailStr = Field(max_length=255)
    password_hash: str = Field(max_length=100)