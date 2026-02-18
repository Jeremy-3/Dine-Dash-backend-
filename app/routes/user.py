from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import crud_user 
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.schemas.response import ResponseModel
from uuid import UUID
from typing import List   
from app.dependencies.rbac import require_permission

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=ResponseModel[UserOut],dependencies=[Depends(require_permission("users.create"))])
def create__user( user_create: UserCreate, db: Session = Depends(get_db)):
    new_user = crud_user.create_user(db, user_create)

    return ResponseModel(data=new_user, message="User created successfully")

@router.get("/", response_model=ResponseModel[List[UserOut]],dependencies=[Depends(require_permission("users.view_all"))])
def get_all_users(db: Session = Depends(get_db)):
    users = crud_user.read(db)
    return ResponseModel(data=users, message="Users retrieved successfully")


@router.get("/{uid}", response_model=ResponseModel[UserOut],dependencies=[Depends(require_permission("users.view"))])
def get_user(uid: UUID, db: Session = Depends(get_db)):
    user = crud_user.get_record_by_field(db, "uid", uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return ResponseModel(data=user, message="User retrieved successfully")

@router.put("/{uid}", response_model=ResponseModel[UserOut],dependencies=[Depends(require_permission("users.edit"))])
def update_user(uid: UUID, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud_user.update_user(db, user_update, uid)
    return ResponseModel(data=updated_user, message="User updated successfully")


@router.post("/apply-driver-role/{uid}", response_model=ResponseModel[UserOut],dependencies=[Depends(require_permission("users.edit"))])
def apply_driver_role(uid: UUID, db: Session = Depends(get_db)):
    user = crud_user.get_record_by_field(db, "uid", uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    updated_user = crud_user.apply_driver_role(db, user)
    return ResponseModel(data=updated_user, message="Driver role applied successfully")

