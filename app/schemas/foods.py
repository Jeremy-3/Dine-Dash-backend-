from pydantic import BaseModel,field_validator
from typing import Optional
from decimal import Decimal

class foodBase(BaseModel):
    name: str
    description: Optional[str] = None
    category:str
    price: Decimal
    available: bool = True

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

class foodCreate(foodBase):
    pass

class foodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category:Optional[str] = None
    price: Optional[Decimal] = None
    avialable: Optional[bool] = None

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than 0")
        return v
    
class foodOut(foodBase):
    id: int

    class Config:
        orm_mode = True
