from pydantic import BaseModel
from typing import Optional,Union,List
from datetime import datetime
from uuid import UUID
from app.schemas.permissions import PermissionOut
from app.schemas.roles import RoleOut

class RolePermissionBase(BaseModel):
    role_id:int
    permissions_id:int
    
class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionAssign(BaseModel):
    role_id:int
    permissions_id:List[int]
    
class RolePermissionDeassignOut(BaseModel):
    removed: List[int]
    not_found: List[int]
    detail: str    

class RolePermissionUpdate(BaseModel):
    role_id: Optional[int] = None
    permissions_id: Optional[List[int]] = None
    

class RolePermissionOut(BaseModel):
    id:int
    uid:Union[str,UUID]
    role:RoleOut = None 
    permission:PermissionOut = None
    created_at:datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

