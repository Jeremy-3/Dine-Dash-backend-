from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from sqlalchemy.orm import Session
from app.core.security import hash_password
from uuid import UUID
from fastapi import HTTPException, status
from app.models.driver import Driver
from app.crud.base import CRUDBase

MODEL = User

class CRUDUser(CRUDBase[MODEL]):
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
        record_data['password_hash'] =hash_password(record_data['password_hash'])

        new_user = self.create(db, UserCreate(**record_data))

        # db.commit()
        # db.refresh(new_user)

        return new_user
    

    def update_user(self, db:Session, uid:UUID, record_in:UserUpdate):
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
        if record_in.password_hash:
            record_in.password_hash = hash_password(record_in.password_hash)

        updated_user = self.update(db, record, record_in)

        # db.commit()
        # db.refresh(updated_user)
        return updated_user
    
    def apply_driver_role(self, db:Session, user:User):
        if user.role and user.role.name.lower() == "driver":
            existing_driver = db.query(Driver).filter(Driver.user_id == user.id).first()
            if not existing_driver:
                new_driver = Driver(user_id=user.id)
                db.add(new_driver)
                db.commit()
                db.refresh(new_driver)
                return new_driver
        return None

crud_user = CRUDUser(MODEL)
