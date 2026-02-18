from app.crud.permissions import crud_permission
from app.schemas.permissions import PermissionCreate, PermissionUpdate
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID


router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.post("/", response_model=ResponseModel, dependencies=[Depends(require_permission("permissions.create"))])
def create_permission(permission_create: PermissionCreate, db: Session = Depends(get_db)): 
    new_permission = crud_permission.create_permission(db, permission_create)
    return ResponseModel(data=new_permission, message="Permission created successfully")

@router.get("/", response_model=ResponseModel, dependencies=[Depends(require_permission("permissions.view"))])
def get_all_permissions(db: Session = Depends(get_db)):
    permissions = crud_permission.read(db)
    return ResponseModel(data=permissions, message="Permissions retrieved successfully")


@router.get("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("permissions.view"))])
def get_permission(uid: UUID, db: Session = Depends(get_db)):
    permission = crud_permission.get_record_by_field(db, "uid", uid)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )
    return ResponseModel(data=permission, message="Permission retrieved successfully")  

@router.put("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("permissions.edit"))])
def update_permission(uid: UUID, permission_update: PermissionUpdate, db: Session = Depends(get_db)):
    updated_permission = crud_permission.update_permission(db, permission_update, uid)
    return ResponseModel(data=updated_permission, message="Permission updated successfully")