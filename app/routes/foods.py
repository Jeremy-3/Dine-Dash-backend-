from app.crud.foods import crud_food
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID
from app.schemas.foods import FoodCreate, FoodUpdate

router = APIRouter(prefix="/foods", tags=["foods"])

@router.post("/", response_model=ResponseModel, dependencies=[Depends(require_permission("foods.create"))])
def create_food(food_create: FoodCreate, db: Session = Depends(get_db)):
    new_food = crud_food.create_food(db, food_create)
    return ResponseModel(data=new_food, message="Food created successfully")

@router.get("/", response_model=ResponseModel, dependencies=[Depends(require_permission("foods.view"))])
def get_all_foods(db: Session = Depends(get_db)):
    foods = crud_food.read(db)
    return ResponseModel(data=foods, message="Foods retrieved successfully")    

@router.get("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("foods.view"))])
def get_food(uid: UUID, db: Session = Depends(get_db)):
    food = crud_food.get_record_by_field(db, "uid", uid)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    return ResponseModel(data=food, message="Food retrieved successfully")  

@router.put("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("foods.edit"))])
def update_food(uid: UUID, food_update: FoodUpdate, db: Session = Depends(get_db)):
    updated_food = crud_food.update_food(db, food_update, uid)
    return ResponseModel(data=updated_food, message="Food updated successfully")


