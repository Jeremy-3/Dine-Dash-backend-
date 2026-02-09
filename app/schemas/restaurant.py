from pydantic import BaseModel,field_validator
from typing import Optional, Union
from app.utils.validate import validate_kenyan_phone_number
from uuid import UUID

class RestaurantBase(BaseModel):
    name: str
    street: str
    city: str
    state: str
    zip_code: str
    phone: str

    @field_validator("phone")
    def validate_phone(cls, v: str) -> str:
        return validate_kenyan_phone_number(v)
    
class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None

    @field_validator("phone")
    def validate_phone(cls, v: str) -> str:
        if v is not None:
            return validate_kenyan_phone_number(v)
        return v


class RestuarantOut(RestaurantBase):
    id: int
    uid: Union[str, UUID]

    class Config:
        orm_mode = True