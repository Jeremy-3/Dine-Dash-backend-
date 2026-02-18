from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

MODEL = Address

class CRUDAddress(CRUDBase[MODEL]):
    def create_address(self, db:Session, record_create:AddressCreate):
        return self.create(db, record_create)
    

    def delete_address(self, db:Session, uid:int):
        record = self.get_record_by_field(db, "uid", uid)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        db.delete(record)
        db.commit()

crud_address = CRUDAddress(MODEL)

