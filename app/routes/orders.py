from app.crud.orders import crud_order
from app.schemas.order import OrderCreate, OrderUpdate, OrderOut,OrderAssign
from app.dependencies.rbac import require_permission
from app.dependencies.auth import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session , joinedload
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID
from app.models.order import Order
from app.models.order_item import OrderItem
from app.crud.deliveries import crud_delivery
from app.crud.driver import crud_driver

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post(
    "",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("orders.create"))]
)
def create_order(order_create: OrderCreate, db: Session = Depends(get_db)):
    new_order = crud_order.create_order(db, order_create)
    return ResponseModel(data=OrderOut.from_orm_with_items(new_order), message="Order created successfully")

@router.get(
    "",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("orders.view_all"))]
)
def get_all_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    orders, total = crud_order.get_all_with_items(db, page, limit)
    return ResponseModel(
        data=[OrderOut.from_orm_with_items(o) for o in orders],
        message="Orders retrieved successfully",
        total=total
    )

# ── NEW: customer fetches their own orders ─────────────────────────────────────
@router.get(
    "/my-orders",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("orders.view_own"))]
)
def get_my_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders, total = crud_order.get_orders_by_customer(db, current_user.id, page, limit)
    return ResponseModel(
        data=[OrderOut.from_orm_with_items(o) for o in orders],
        message="Orders retrieved successfully",
        total=total
    )

# DRIVERS GET THE ORDES THEY WERE ASSIGNED

@router.get(
    "/my-deliveries",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("deliveries.view_own"))]
)
def get_my_deliveries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = (
        db.query(Order)
        .options(
            joinedload(Order.order_items).joinedload(OrderItem.food),
            joinedload(Order.customer),
            joinedload(Order.driver),
            joinedload(Order.restaurant),
        )
        .filter(Order.driver_id == current_user.id)   # ← driver_id stores user.id
        .order_by(Order.created_at.desc())
        .all()
    )

    return ResponseModel(
        data=[OrderOut.from_orm_with_items(o) for o in orders],
        message="Deliveries retrieved successfully",
        total=len(orders)
    )

@router.get(
    "/{uid}",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("orders.view_own"))]
)
def get_order(uid: UUID, db: Session = Depends(get_db)):
    order = crud_order.get_record_by_field(db, "uid", uid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return ResponseModel(data=OrderOut.from_orm_with_items(order), message="Order retrieved successfully")






@router.put(
    "/{uid}",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("orders.edit"))]
)
def update_order(uid: UUID, order_update: OrderUpdate, db: Session = Depends(get_db)):
    updated_order = crud_order.update_order(db, uid, order_update)
    return ResponseModel(data=OrderOut.from_orm_with_items(updated_order), message="Order updated successfully")

@router.delete(
    "/{uid}",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("orders.cancel"))]
)
def delete_order(uid: UUID, db: Session = Depends(get_db)):
    order = crud_order.get_record_by_field(db, "uid", uid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    crud_order.delete_record(db, order)
    return ResponseModel(message="Order deleted successfully")


@router.post(
    "/{uid}/assign",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("deliveries.assign"))]
)
def assign_order(
    uid: UUID,
    assign_data: OrderAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ── Get order ──────────────────────────────────────────────────────────────
    order = crud_order.get_record_by_field(db, "uid", uid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status not in {"pending", "confirmed"}:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot assign order in status '{order.status}'"
        )

    # ── Get driver record (drivers table uses driver.id not user.id) ───────────
    driver = crud_driver.get_record_by_field(db, "id", assign_data.driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    if driver.status != "available":
        raise HTTPException(status_code=400, detail="Driver is not available")

    # ── Update order ───────────────────────────────────────────────────────────
    order.driver_id     = driver.user_id        # ← store user_id on order, not driver.id
    order.restaurant_id = assign_data.restaurant_id
    order.status        = "assigned"
    db.add(order)

    # ── Set driver to busy ─────────────────────────────────────────────────────
    driver.status = "busy"
    db.add(driver)

    # ── Create Delivery record ─────────────────────────────────────────────────
    existing_delivery = crud_delivery.get_record_by_field(db, "order_id", order.id)
    if not existing_delivery:
        from app.models.deliveries import Delivery
        delivery = Delivery(
            order_id=order.id,
            driver_id=driver.id,              # ← drivers.id (not user.id)
            restaurant_id=assign_data.restaurant_id,
            assigned_by=current_user.id,
            status="assigned",
        )
        db.add(delivery)

    db.commit()
    db.refresh(order)

    # ── Reload with relationships ──────────────────────────────────────────────

    order = (
        db.query(Order)
        .options(
            joinedload(Order.order_items).joinedload(OrderItem.food),
            joinedload(Order.customer),
            joinedload(Order.driver),
            joinedload(Order.restaurant),
        )
        .filter(Order.id == order.id)
        .first()
    )

    return ResponseModel(
        data=OrderOut.from_orm_with_items(order),
        message="Order assigned successfully"
    )