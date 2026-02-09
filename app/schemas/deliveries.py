from pydantic import BaseModel, field_validator
from typing import Optional
from app.schemas.constants import DELIVERY_STATUSES
from app.schemas.order import OrderOut
from app.schemas.driver import DriverOut
from app.schemas.restaurant import RestaurantOut

class DeliveryBase(BaseModel):
    order_id:int
    driver_id: int
    restaurant_id: int
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in DELIVERY_STATUSES:
            raise ValueError(f"Invalid delivery status: {v}")
        return v

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryUpdate(BaseModel):
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in DELIVERY_STATUSES:
            raise ValueError(f"Invalid delivery status: {v}")
        return v
    
class DeliveryOut(DeliveryBase):
    id: int
    order: Optional[OrderOut] = None
    driver: Optional[DriverOut] = None
    restaurant: Optional[RestaurantOut] = None

    class Config:
        orm_mode = True