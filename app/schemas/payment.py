from pydantic import BaseModel,field_validator
from typing import Optional, Union
from uuid import UUID
from decimal import Decimal
from app.schemas.constants import PAYMENT_STATUSES
from datetime import datetime
class PaymentBase(BaseModel):
    order_id: int
    amount: Decimal
    status: str
    method: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in PAYMENT_STATUSES:
            raise ValueError(f"Invalid status. Must be one of {PAYMENT_STATUSES}")
        return v
    
    @field_validator("amount")
    @classmethod
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("Amount must be >= 0")
        return v
    
class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = None
    status: Optional[str] = None
    method: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in PAYMENT_STATUSES:
            raise ValueError(f"Invalid status. Must be one of {PAYMENT_STATUSES}")
        return v
    
    @field_validator("amount")
    @classmethod
    def non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Amount must be >= 0")
        return v
    
class PaymentOut(PaymentBase):
    id: int
    uid: Union[str, UUID]
    paid_at: Optional[datetime] = None

    class Config:
        orm_mode = True