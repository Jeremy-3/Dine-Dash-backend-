from app.crud.address import crud_address
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID
from app.schemas.address import AddressCreate, AddressUpdate

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.post("/", response_model=ResponseModel, dependencies=[Depends(require_permission("addresses.create"))])
def create_address(address_create: AddressCreate, db: Session = Depends(get_db)):
    new_address = crud_address.create_address(db, address_create)
    return ResponseModel(data=new_address, message="Address created successfully")


@router.delete("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("addresses.delete"))])
def delete_address(uid: UUID, db: Session = Depends(get_db)):
    crud_address.delete_address(db, uid)
    return ResponseModel(message="Address deleted successfully")

