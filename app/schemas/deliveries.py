from pydantic import BaseModel, field_validator
from typing import Optional,Union
from app.schemas.constants import DELIVERY_STATUSES
from app.schemas.order import OrderOut
from app.schemas.driver import DriverOut
from app.schemas.restaurant import RestaurantOut
from uuid import UUID

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
    uid:Union[str]
    order: Optional[OrderOut] = None
    driver: Optional[DriverOut] = None
    restaurant: Optional[RestaurantOut] = None

    model_config = {"from_attributes": True}
