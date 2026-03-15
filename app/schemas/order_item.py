from pydantic import BaseModel, field_validator
from typing import Optional
from app.schemas.foods import FoodOut
from decimal import Decimal


class OrderItemBase(BaseModel):
    order_id: int
    food_id: int
    quantity: int
    price_at_order: Optional[Decimal] = None  # optional — CRUD snapshots from food.price

    @field_validator("price_at_order")
    @classmethod
    def validate_price_at_order(cls, v):
        if v is not None and v <= 0:           # ← guard None before comparing
            raise ValueError("Price at order must be greater than 0")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    price_at_order: Optional[Decimal] = None

    @field_validator("price_at_order")
    @classmethod
    def validate_price_at_order(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price at order must be greater than 0")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v


class OrderItemOut(BaseModel):
    id: int
    order_id: int
    food_id: int
    quantity: int
    price_at_order: Optional[Decimal] = None
    food: Optional[FoodOut] = None

    model_config = {"from_attributes": True}