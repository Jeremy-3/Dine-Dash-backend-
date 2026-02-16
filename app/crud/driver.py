from app.models.driver import Driver
from app.models.user import User
from app.schemas.driver import DriverCreate, DriverUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.core.constants import ROLE_DRIVER_ID


class CRUDDriver(CRUDBase[Driver]):
    def create_driver(self, db: Session, record_create: DriverCreate):
        # ensure user exists
        user = db.query(User).filter(User.id == record_create.user_id).first()
        if not user:
            raise HTTPException(404, "User not found")

        # ensure correct role
        if user.role_id != ROLE_DRIVER_ID:
            raise HTTPException(
                status_code=400,
                detail="User must have DRIVER role to become a driver",
            )

        # ensure one-to-one relationship
        existing = self.get_record_by_field(db, "user_id", record_create.user_id)
        if existing:
            raise HTTPException(400, "User is already a driver")

        return self.create(db, record_create)

    def update_driver(self, db: Session, uid: UUID, record_in: DriverUpdate):
        driver = self.get_record_by_field(db, "uid", uid)
        if not driver:
            raise HTTPException(404, "Driver not found")

        return self.update(db, driver, record_in)

    def get_driver_by_user_id(self, db: Session, user_id: int):
        return self.get_record_by_field(db, "user_id", user_id)

    def get_available_drivers(self, db: Session):
        return (
            db.query(Driver)
            .filter(Driver.status == "available")
            .all()
        )

    def deactivate_driver(self, db: Session, uid: UUID):
        driver = self.get_record_by_field(db, "uid", uid)
        if not driver:
            raise HTTPException(404, "Driver not found")

        driver.status = "offline"
        db.commit()
        return driver


crud_driver = CRUDDriver(Driver)
