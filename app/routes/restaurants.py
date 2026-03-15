from app.crud.restaurants import crud_restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate,RestaurantOut
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID  

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=ResponseModel[RestaurantOut], dependencies=[Depends(require_permission("restaurants.create"))])
def create_restaurant(restaurant_create: RestaurantCreate, db: Session = Depends(get_db)):
    new_restaurant = crud_restaurant.create_restaurant(db, restaurant_create)
    return ResponseModel(data=new_restaurant, message="Restaurant created successfully")

@router.get("/", response_model=ResponseModel[list[RestaurantOut]], dependencies=[Depends(require_permission("restaurants.view"))])
def get_all_restaurants(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    restaurants, total = crud_restaurant.read(db,page,limit)
    return ResponseModel(data=restaurants, total=total,message="Restaurants retrieved successfully")

@router.get("/{uid}", response_model=ResponseModel[RestaurantOut], dependencies=[Depends(require_permission("restaurants.view"))])
def get_restaurant(uid: UUID, db: Session = Depends(get_db)):
    restaurant = crud_restaurant.get_record_by_field(db, "uid", uid)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    return ResponseModel(data=restaurant, message="Restaurant retrieved successfully")

@router.put("/{uid}", response_model=ResponseModel[RestaurantOut], dependencies=[Depends(require_permission("restaurants.edit"))])
def update_restaurant(uid: UUID, restaurant_update: RestaurantUpdate, db: Session = Depends(get_db)):
    updated_restaurant = crud_restaurant.update_restaurant(db, restaurant_update, uid)
    return ResponseModel(data=updated_restaurant, message="Restaurant updated successfully")

