from pydantic import BaseModel,field_validator
from typing import Optional
from app.schemas.foods import foodOut
from app.schemas.order import OrderOut
from decimal import Decimal
class OrderItemBase(BaseModel):
    order_id: int
    food_id: int
    quantity: int
    price_at_order: Decimal

    @field_validator("price_at_order")
    @classmethod
    def validate_price_at_order(cls, v):
        if v <= 0:
            raise ValueError("Price at order must be greater than 0")
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
    
class OrderItemOut(OrderItemBase):
    id: int
    order: Optional[OrderOut] = None
    food: Optional[foodOut] = None

    class Config:
        orm_mode = True
