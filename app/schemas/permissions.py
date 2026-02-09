from pydantic import BaseModel
from typing import Union, Optional
from uuid import UUID

class PermissionBase(BaseModel):
    name: str
    description: str  

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class PermissionOut(PermissionBase):
    id: int
    uid: Union[str, UUID]

    class Config:
        orm_mode = True