from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.role_permission import RolePermission
from app.models.permissions import Permissions

def require_permission(permission_name: str):
    def dependency(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        # Superadmin bypass (optional but recommended)
        if current_user.is_superadmin:
            return True

        perms = (
            db.query(Permissions.name)
            .join(RolePermission, RolePermission.permission_id == Permissions.id)
            .filter(RolePermission.role_id == current_user.role_id)
            .all()
        )

        user_permissions = {p[0] for p in perms}

        if permission_name not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission_name}",
            )

        return True

    return dependency
