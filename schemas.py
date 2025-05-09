from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    IN_TRANSIT = "IN-TRANSIT"
    DELIVERED = "DELIVERED"


class PizzaSize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    EXTRA_LARGE = "EXTRA-LARGE"


class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }
    )


class Settings(BaseModel):
    authjwt_secret_key: str = 'b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    order_status: Literal["PENDING", "IN-TRANSIT", "DELIVERED"] = "PENDING"
    pizza_size: Literal["SMALL", "MEDIUM", "LARGE", "EXTRA-LARGE"] = "SMALL"
    user_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "quantity": 2,
                "pizza_size": "LARGE"
            }
        }
    )


class OrderStatusModel(BaseModel):
    order_status: Literal["PENDING", "IN-TRANSIT", "DELIVERED"] = "PENDING"

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "order_status": "PENDING"
            }
        }
    )