from app.models.restaurants import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

MODEL = Restaurant

class CrudRestaurant(CRUDBase[MODEL]):
    """CRUD operations for Restaurant model"""
    
    def create_restaurant(self, db:Session, record_create:RestaurantCreate):
        # check if restaurant with same name exists
        existing_record = self.get_record_by_fields(db, {"name": record_create.name, "phone": record_create.phone})

        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant with this name and phone already exists"
            )

        return self.create(db, record_create)
    
    def update_restaurant(self, db:Session, record_update:RestaurantUpdate, uid:UUID):
        record = self.get_record_by_field(db, "uid", uid)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        # prevent duplicate name and phone
        new_name = record_update.name or record.name
        new_phone = record_update.phone or record.phone

        if new_name != record.name or new_phone != record.phone:
            existing_record = self.get_record_by_fields(db, {"name": new_name, "phone": new_phone})
            if existing_record and existing_record.id != record.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Another restaurant with this name and phone already exists"
                )
        
        return self.update(db, record, record_update)
    
    def delete_restaurant(self, db:Session, uid:UUID):
        record = self.get_record_by_field(db, "uid", uid)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        db.delete(record)
        db.commit()

crud_restaurant = CrudRestaurant(MODEL)