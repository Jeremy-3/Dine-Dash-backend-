from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional,Union
from app.utils.validate import validate_password, validate_kenyan_phone_number
from app.schemas.roles import RoleOut
from uuid import UUID
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    role_id: int 



class UserCreate(UserBase):
    name:str
    email:EmailStr
    phone:Optional[str] = None
    password:str
    role_id:int | None = None

    @field_validator("password")
    def validate_password_filed(cls,v:str) -> str:
        return validate_password(v)  
    
    @field_validator("phone")
    def validate_phone(cls, v: str) -> str:
        if v is not None:
            return validate_kenyan_phone_number(v)
        return v


class UserCreateDB(BaseModel):
    name: str
    email: EmailStr
    password_hash: str
    role_id: int | None = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None

    @field_validator("password")
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

    model_config = {"from_attributes": True}


