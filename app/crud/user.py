from app.models.user import User
from app.schemas.user import UserCreate, UserCreateDB, UserUpdate
from sqlalchemy.orm import Session
from app.core.security import hash_password
from uuid import UUID
from fastapi import HTTPException, status
from app.models.driver import Driver
from app.crud.base import CRUDBase
from app.core.constants import ROLE_CUSTOMER_ID
MODEL = User

class CRUDUser(CRUDBase[MODEL,UserCreate]):
    """CRUD operations for User model"""

    def create_user(self,db:Session,record_create:UserCreate):
        # check if user exists
        existing_record = self.get_record_by_field(db, "email", record_create.email)
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
    
        record_data = record_create.model_dump()
        record_data['password_hash'] =hash_password(record_data['password'])

        record_data.pop("password")

        if not record_data.get("role_id"):
                record_data["role_id"] = ROLE_CUSTOMER_ID

        db_obj = UserCreateDB(**record_data) 

        new_user = self.create(db, db_obj)

        # db.commit()
        # db.refresh(new_user)

        return new_user
    

    def update_user(self, db: Session, uid: UUID, record_in: UserUpdate):
        record = self.get_record_by_field(db, "uid", uid)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if record_in.email and record_in.email != record.email:
            existing_record = self.get_record_by_field(db, "email", record_in.email)
            if existing_record:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        # ← was record_in.password_hash (doesn't exist on UserUpdate)
        if record_in.password:
            record.password_hash = hash_password(record_in.password)

        # Build update dict excluding password (already handled above)
        update_data = record_in.model_dump(exclude_unset=True, exclude={"password"})
        for field, value in update_data.items():
            setattr(record, field, value)

        db.commit()
        db.refresh(record)
        return record
    
    def apply_driver_role(self, db: Session, user: User):
        from app.core.constants import ROLE_DRIVER_ID
        # Update role to driver
        user.role_id = ROLE_DRIVER_ID
        db.add(user)

        # Create driver profile if not exists
        existing_driver = db.query(Driver).filter(Driver.user_id == user.id).first()
        if not existing_driver:
            new_driver = Driver(user_id=user.id, status="available")
            db.add(new_driver)

        db.commit()
        db.refresh(user)
        return user 

crud_user = CRUDUser(MODEL)
