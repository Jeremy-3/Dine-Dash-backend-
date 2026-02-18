from app.crud.orders import crud_order
from app.schemas.order import OrderCreate, OrderUpdate
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.create"))])
def create_order(order_create: OrderCreate, db: Session = Depends(get_db)):
    new_order = crud_order.create_order(db, order_create)
    return ResponseModel(data=new_order, message="Order created successfully")

@router.get("/", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.view"))])
def get_all_orders(db: Session = Depends(get_db)):
    orders = crud_order.read(db)
    return ResponseModel(data=orders, message="Orders retrieved successfully")      

# @router.get("/by-customer/{customer_id}", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.view"))])
# def get_orders_by_customer(customer_uid: UUID, db: Session = Depends(get_db)):
#     orders = crud_order.get_orders_by_customer(db, customer_uid)
#     return ResponseModel(data=orders, message="Orders retrieved successfully")


@router.get("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.view"))])
def get_order(uid: UUID, db: Session = Depends(get_db)):
    order = crud_order.get_record_by_field(db, "uid", uid)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return ResponseModel(data=order, message="Order retrieved successfully")

@router.put("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.edit"))])
def update_order(uid: UUID, order_update: OrderUpdate, db: Session = Depends(get_db)):
    updated_order = crud_order.update_order(db, order_update, uid)
    return ResponseModel(data=updated_order, message="Order updated successfully")


@router.delete("/{uid}", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.cancel"))])
def delete_order(uid: UUID, db: Session = Depends(get_db)):
    order = crud_order.get_record_by_field(db, "uid", uid)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    crud_order.delete_record(db, order)
    return ResponseModel(message="Order deleted successfully")


