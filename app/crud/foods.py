from app.models.foods import Food
from app.schemas.foods import FoodCreate, FoodUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException, status   
from uuid import UUID
MODEL = Food


class CRUDFood(CRUDBase[MODEL]):
    def create_food(self, db:Session, record_create:FoodCreate):
        # check if food already exists with same name
        existing_record = self.get_record_by_field(db, "name", record_create.name)
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Food with this name already exists"
            )
        
        new_food = self.create(db, record_create)
        return new_food

    def update_food(self, db:Session, uid:UUID, record_in:FoodUpdate):
        # check if food exists
        existing_record = self.get_record_by_field(db, "uid", uid)
        if not existing_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food not found"
            )
        
        # if name is being updated, check for uniqueness
        if record_in.name and record_in.name != existing_record.name:
            name_conflict = self.get_record_by_field(db, "name", record_in.name)
            if name_conflict:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Food with this name already exists"
                )
        updated_food = self.update(db, existing_record, record_in)
        return updated_food
    

    def delete_food(self, db:Session, uid:UUID):
        existing_record = self.get_record_by_field(db, "uid", uid)
        if not existing_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food not found"
            )
        db.delete(existing_record)
        db.commit()
        

crud_food = CRUDFood(MODEL)
