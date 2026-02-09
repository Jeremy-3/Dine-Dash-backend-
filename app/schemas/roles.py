from pydantic import BaseModel
from typing import Optional,Union
from uuid import UUID

class RoleBase(BaseModel):
    name: str
    active: bool = True

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None

class RoleOut(RoleBase):
    id:int
    uid:Union[str, UUID]



    class Config:
        orm_mode = True
