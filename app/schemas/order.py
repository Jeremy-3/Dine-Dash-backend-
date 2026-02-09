from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator
from app.schemas.constants import ORDER_STATUSES
from uuid import UUID
from typing import Optional, Union

class OrderBase(BaseModel):
    customer_id: int
    status: str
    subtotal: Decimal
    delivery_fee: Decimal
    total: Decimal

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str):
        if v not in ORDER_STATUSES:
            raise ValueError(f"Invalid order status: {v}")
        return v

    @field_validator("subtotal", "delivery_fee", "total")
    @classmethod
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("Amount must be >= 0")
        return v


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    subtotal: Optional[Decimal] = None
    delivery_fee: Optional[Decimal] = None
    total: Optional[Decimal] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str):
        if v is not None and v not in ORDER_STATUSES:
            raise ValueError(f"Invalid order status: {v}")
        return v

    @field_validator("subtotal", "delivery_fee", "total")
    @classmethod
    def non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Amount must be >= 0")
        return v


class OrderOut(OrderBase):
    id: int
    uid: Union[str, UUID]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True