from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional,Union
from app.utils.validate import validate_password, validate_kenyan_phone_number
from app.schemas.roles import RoleOut
from uuid import UUID
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone:str
    role_id: int

class UserCreate(UserBase):
    name:str
    email:EmailStr
    phone:Optional[str] = None
    password_hash:str
    role_id:int

    @field_validator("password_hash")
    def validate_password_filed(cls,v:str) -> str:
        return validate_password(v)  
    
    @field_validator("phone")
    def validate_phone(cls, v: str) -> str:
        if v is not None:
            return validate_kenyan_phone_number(v)
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password_hash: Optional[str] = None
    role_id: Optional[int] = None

    @field_validator("password_hash")
    def validate_password_filed(cls,v:str) -> str:
        if v is not None:
            return validate_password(v)
        return v
    
    @field_validator("phone")
    def validate_phone(cls, v: str) -> str:
        if v is not None:
            return validate_kenyan_phone_number(v)
        return v
    
class UserOut(UserBase):
    id: int
    uid: Union[str, UUID]
    role:RoleOut= None

    class Config:
        orm_mode = True

