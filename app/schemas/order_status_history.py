from pydantic import BaseModel, field_validator
from typing import Optional
from app.schemas.constants import ORDER_STATUSES
from datetime import datetime

class OrderStatusHistoryBase(BaseModel):
    order_id: int
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ORDER_STATUSES:
            raise ValueError(f"Invalid order status: {v}")
        return v
    
class OrderStatusHistoryCreate(OrderStatusHistoryBase):
    pass

class OrderStatusHistoryUpdate(BaseModel):  
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in ORDER_STATUSES:
            raise ValueError(f"Invalid order status: {v}")
        return v
    
class OrderStatusHistoryOut(OrderStatusHistoryBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
