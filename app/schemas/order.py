# app/schemas/order.py
from pydantic import BaseModel, field_validator
from app.schemas.constants import ORDER_STATUSES

class OrderBase(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str):
        if v not in ORDER_STATUSES:
            raise ValueError(f"Invalid order status: {v}")
        return v
