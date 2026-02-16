from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.role_permission import RolePermission
from app.schemas.role_permission import (
    RolePermissionAssign,
    RolePermissionDeassignOut
)
from app.crud.base import CRUDBase


class CRUDRolePermission(CRUDBase[RolePermission, RolePermissionAssign]):
    """RBAC role-permission assignment logic"""

    def assign_permissions(self,db: Session,record_in: RolePermissionAssign) -> list[int]:

        assigned = []

        try:
            for permission_id in record_in.permissions_id:
                exists = self.get_record_by_fields(db,
                    {
                        "role_id": record_in.role_id,
                        "permission_id": permission_id,
                    },
                )

                if not exists:
                    rp = RolePermission(
                        role_id=record_in.role_id,
                        permission_id=permission_id,
                    )
                    db.add(rp)
                    assigned.append(permission_id)

            db.commit()
            return assigned

        except Exception:
            db.rollback()
            raise

    def deassign_permissions(self,db: Session,record_in: RolePermissionAssign) -> RolePermissionDeassignOut:

        removed = []
        not_found = []

        try:
            for permission_id in record_in.permissions_id:
                rp = self.get_record_by_fields(
                    db,
                    {
                        "role_id": record_in.role_id,
                        "permission_id": permission_id,
                    },
                )

                if rp:
                    db.delete(rp)
                    removed.append(permission_id)
                else:
                    not_found.append(permission_id)

            db.commit()

            return RolePermissionDeassignOut(
                removed=removed,
                not_found=not_found,
                detail=(
                    f"Removed {len(removed)} permissions. "
                    f"{len(not_found)} permissions were not found."
                ),
            )

        except Exception:
            db.rollback()
            raise


crud_role_permission = CRUDRolePermission(RolePermission)
