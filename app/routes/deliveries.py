from app.dependencies.rbac import require_permission
from app.crud.deliveries import crud_delivery
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID   

router = APIRouter(prefix="/deliveries", tags=["deliveries"])

@router.post("/", response_model=ResponseModel, dependencies=[Depends(require_permission("deliveries.create"))])
def create_delivery(delivery_create: DeliveryCreate, db: Session = Depends(get_db)):
    new_delivery = crud_delivery.create_delivery(db, delivery_create)
    return ResponseModel(data=new_delivery, message="Delivery created successfully")    

@router.get("/", response_model=ResponseModel, dependencies=[Depends(require_permission("deliveries.view"))])
def get_all_deliveries(db: Session = Depends(get_db)):
    deliveries = crud_delivery.read(db)
    return ResponseModel(data=deliveries, message="Deliveries retrieved successfully")


@router.post("/assign/{delivery_uid}/{driver_id}", response_model=ResponseModel, dependencies=[Depends(require_permission("deliveries.assign"))])
def assign_delivery(delivery_uid: UUID, driver_id: int, db: Session = Depends(get_db)):
    assigned_delivery = crud_delivery.assign_delivery(db, delivery_uid, driver_id)
    return ResponseModel(data=assigned_delivery, message="Delivery assigned successfully")


@router.get("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("deliveries.view"))])
def get_delivery(uid: UUID, db: Session = Depends(get_db)):
    delivery = crud_delivery.get_record_by_field(db, "uid", uid)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found"
        )
    return ResponseModel(data=delivery, message="Delivery retrieved successfully")

@router.put("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("deliveries.edit"))])
def update_delivery(uid: UUID, delivery_update: DeliveryUpdate, db: Session = Depends(get_db)):
    delivery = crud_delivery.get_record_by_field(db, "uid", uid)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found"
        )
    updated_delivery = crud_delivery.update_delivery(db, uid, delivery_update)
    return ResponseModel(data=updated_delivery, message="Delivery updated successfully")