from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.role_permission import RolePermission
from app.models.permissions import Permissions
from app.dependencies.auth import get_current_user


class RBAC:
    """
    Role-Based Access Control helper
    """

    @staticmethod
    def has_permission(permission_name: str):
        """
        Usage:
            @router.post("/foods")
            def create_food(
                _: User = Depends(RBAC.has_permission("food:create"))
            ):
                ...
        """

        def dependency(
            current_user: User = Depends(get_current_user),
            db: Session = Depends(get_db),
        ):
            # Superadmin bypass
            if current_user.role_id == 1:
                return current_user

            permission = (
                db.query(Permissions)
                .filter(Permissions.name == permission_name)
                .first()
            )

            if not permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission not registered",
                )

            has_access = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id == current_user.role_id,
                    RolePermission.permission_id == permission.id,
                )
                .first()
            )

            if not has_access:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to perform this action",
                )

            return current_user

        return dependency
