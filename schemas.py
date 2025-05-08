from  pydantic import BaseModel
from typing import Optional as optional

class SignupModel(BaseModel):
    id:optional[int]
    username: str
    email: str
    password: str
    is_staff:optional[bool] 
    is_active:optional[bool]

    class config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": " john@gmail.com",
                "password": "password123",
                "is_staff": False,
                "is_active": True
            }
        }