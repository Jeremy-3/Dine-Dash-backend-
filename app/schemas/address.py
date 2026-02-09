from pydantic import BaseModel, field_validator
from typing import Optional
from app.schemas.orders import OrderOut

class AddressBase(BaseModel):
    order_id: int
    street: str
    city: str
    state: str
    zip_code: str
    notes : Optional[str] = None

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    notes : Optional[str] = None

class AddressOut(AddressBase):
    id:int
    order: Optional[OrderOut] = None

    class Config:
        orm_mode = True