from app.models.role_permission import RolePermission
from app.crud.role_permission import CRUDRolePermission
from app.schemas.role_permission import RolePermissionCreate, RolePermissionUpdate
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db
from app.dependencies.rbac import require_permission
from app.schemas.response import ResponseModel
from uuid import UUID


router = APIRouter(prefix="/role-permissions", tags=["role-permissions"])

@router.post("/assign", response_model=ResponseModel[RolePermission], dependencies=[Depends(require_permission("role_permissions.assign"))])
def assign_permission_to_role(role_permission_create: RolePermissionCreate, db: Session = Depends(get_db)):
    new_role_permission = CRUDRolePermission().assign_permissions(db, role_permission_create)
    return ResponseModel(data=new_role_permission, message="Permission assigned to role successfully")


@router.post("/deassign", response_model=ResponseModel[RolePermission], dependencies=[Depends(require_permission("role_permissions.deassign"))])
def deassign_permission_from_role(role_permission_update: RolePermissionUpdate, db: Session = Depends(get_db)):
    result = CRUDRolePermission().deassign_permissions(db, role_permission_update)
    return ResponseModel(data=result, message="Permission deassigned from role successfully")