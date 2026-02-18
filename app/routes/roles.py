from app.schemas.role import RoleCreate, RoleUpdate
from app.crud.roles import crud_role
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.rbac import require_permission
from app.schemas.response import ResponseModel
from uuid import UUID
from typing import List


router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=ResponseModel[RoleCreate], dependencies=[Depends(require_permission("roles.create"))])
def create_role(role_create: RoleCreate, db: Session = Depends(get_db)):
    new_role = crud_role.create_role(db, role_create)
    return ResponseModel(data=new_role, message="Role created successfully")


@router.get("/", response_model=ResponseModel[List[RoleCreate]], dependencies=[Depends(require_permission("roles.view"))])
def get_all_roles(db: Session = Depends(get_db)):
    roles = crud_role.read(db)
    return ResponseModel(data=roles, message="Roles retrieved successfully")

@router.get("/{uid}", response_model=ResponseModel[RoleCreate], dependencies=[Depends(require_permission("roles.view"))])
def get_role(uid: UUID, db: Session = Depends(get_db)):
    role = crud_role.get_record_by_field(db, "uid", uid)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return ResponseModel(data=role, message="Role retrieved successfully")

@router.put("/{uid}", response_model=ResponseModel[RoleCreate], dependencies=[Depends(require_permission("roles.edit"))])
def update_role(uid: UUID, role_update: RoleUpdate, db: Session = Depends(get_db)):
    updated_role = crud_role.update_role(db, role_update, uid)
    return ResponseModel(data=updated_role, message="Role updated successfully")

