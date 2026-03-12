# app/api/v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import Login
from app.core.security import verify_password, create_access_token
from app.db.session import get_db
from app.crud.user import crud_user
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/login", tags=["auth"])


@router.post("", response_model=ResponseModel)
def login(user_login: Login, db: Session = Depends(get_db)):
    """Login endpoint"""
    # Check if user exists
    user = crud_user.get_record_by_field(db, "email", user_login.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify password
    if not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Check if user is active
    if hasattr(user, 'is_active') and not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Get role name (handle if role is object or None)
    role_name = user.role.name if user.role else "customer"
    
    # Get permissions (handle if not available)
    permissions = []
    if hasattr(user, 'role') and user.role:
        # Get permissions from role
        from app.models.role_permission import RolePermission
        from app.models.permissions import Permissions
        
        role_perms = db.query(Permissions).join(RolePermission).filter(
            RolePermission.role_id == user.role_id
        ).all()
        
        permissions = [perm.name for perm in role_perms]
    
    # Create access token
    access_token = create_access_token(
        user_id=user.id,
        name=user.name,
        email=user.email,
        phone=user.phone,
        role=role_name, 
        permissions=permissions  
    )
    
    return ResponseModel(
            success=True, 
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "uid": str(user.uid),
                    "name": user.name,
                    "email": user.email,
                    "role_id": user.role_id,
                    "role": role_name
                }
            },
            message="Login successful"
        )