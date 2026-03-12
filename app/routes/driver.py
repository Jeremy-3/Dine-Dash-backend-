from app.crud.driver import crud_driver
from app.schemas.driver import DriverCreate, DriverOut, DriverUpdate
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID


router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.post("/", response_model=ResponseModel, dependencies=[Depends(require_permission("drivers.create"))])
def create_driver(driver_create: DriverCreate, db: Session = Depends(get_db)):
    new_driver = crud_driver.create_driver(db, driver_create)
    return ResponseModel(data=new_driver, message="Driver created successfully")

@router.get("/", response_model=ResponseModel, dependencies=[Depends(require_permission("drivers.view"))])
def get_all_drivers(db: Session = Depends(get_db)):
    drivers = crud_driver.read(db)
    return ResponseModel(data=drivers, message="Drivers retrieved successfully")    

@router.get("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("drivers.view"))])
def get_driver(uid: UUID, db: Session = Depends(get_db)):
    driver = crud_driver.get_record_by_field(db, "uid", uid)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    return ResponseModel(data=driver, message="Driver retrieved successfully")

@router.put("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("drivers.edit"))])
def update_driver(uid: UUID, driver_update: DriverUpdate, db: Session = Depends(get_db)):
    updated_driver = crud_driver.update_driver(db, driver_update, uid)
    return ResponseModel(data=updated_driver, message="Driver updated successfully")

@router.delete("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("drivers.delete"))])
def delete_driver(uid: UUID, db: Session = Depends(get_db)):
    crud_driver.deactivate_driver(db, uid)
    return ResponseModel(message="Driver deactivated successfully")