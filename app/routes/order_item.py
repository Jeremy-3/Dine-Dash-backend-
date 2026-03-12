# app/api/v1/endpoints/order_items.py
from app.crud.order_item import crud_order_item
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from typing import List

router = APIRouter(prefix="/order-items", tags=["order-items"])


@router.post("/", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.create"))])
def create_order_item(order_item_create: OrderItemCreate, db: Session = Depends(get_db)):
    new_order_item = crud_order_item.add_item(db, order_item_create)
    return ResponseModel(data=new_order_item, message="Order item added successfully")


@router.get("/order/{order_id}", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.view"))])
def get_order_items(order_id: int, db: Session = Depends(get_db)):
    order_items = crud_order_item.get_items_by_order(db, order_id)
    return ResponseModel(data=order_items, message="Order items retrieved successfully")


@router.get("/{item_id}", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.view"))])
def get_order_item(item_id: int, db: Session = Depends(get_db)):
    order_item = crud_order_item.get(db, item_id)
    if not order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found"
        )
    return ResponseModel(data=order_item, message="Order item retrieved successfully")


@router.put("/{item_id}", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.edit"))])
def update_order_item(item_id: int, order_item_update: OrderItemUpdate, db: Session = Depends(get_db)):
    updated_order_item = crud_order_item.update_item(db, item_id, order_item_update)
    return ResponseModel(data=updated_order_item, message="Order item updated successfully")


@router.delete("/{item_id}", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.edit"))])
def delete_order_item(item_id: int, db: Session = Depends(get_db)):
    order_item = crud_order_item.get(db, item_id)
    if not order_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found"
        )
    crud_order_item.remove_item(db, item_id)
    return ResponseModel(message="Order item removed successfully")


@router.post("/bulk/add", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.create"))])
def add_bulk_items(items: List[OrderItemCreate], db: Session = Depends(get_db)):
    added_items = []
    for item_in in items:
        item = crud_order_item.add_item(db, item_in)
        added_items.append(item)
    return ResponseModel(data=added_items, message=f"Added {len(added_items)} items successfully")


@router.delete("/bulk/remove", response_model=ResponseModel, dependencies=[Depends(require_permission("orders.edit"))])
def remove_bulk_items(item_ids: List[int], db: Session = Depends(get_db)):
    removed = []
    errors = []
    
    for item_id in item_ids:
        try:
            crud_order_item.remove_item(db, item_id)
            removed.append(item_id)
        except Exception as e:
            errors.append(f"Item {item_id}: {str(e)}")
    
    return ResponseModel(
        data={"removed": removed, "errors": errors},
        message=f"Removed {len(removed)} items, {len(errors)} errors"
    )