from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from uuid import UUID
from decimal import Decimal
from app.models.order import Order
from app.models.order_item import OrderItem  # ← import needed
from app.models.foods import Food            # ← import needed
from app.schemas.order import OrderCreate, OrderUpdate
from app.crud.base import CRUDBase

MODEL = Order

ORDER_STATUS_FLOW = {
    "pending":          {"confirmed", "cancelled"},
    "confirmed":        {"preparing", "cancelled", "assigned"},  
    "assigned":         {"picked_up", "cancelled"},              
    "preparing":        {"out_for_delivery"},
    "picked_up":        {"in_transit"},                          
    "in_transit":       {"delivered"},                           
    "out_for_delivery": {"delivered"},
    "delivered":        set(),
    "cancelled":        set(),
}

class CRUDOrder(CRUDBase[MODEL, OrderCreate]):

    def create_order(self, db: Session, order_in: OrderCreate) -> Order:
        new_order = MODEL(
            customer_id=order_in.customer_id,
            status="pending",
            subtotal=Decimal("0"),
            delivery_fee=order_in.delivery_fee,
            total=order_in.delivery_fee,
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order

    def get_orders_by_customer(self, db: Session, customer_id: int, page: int = 1, limit: int = 20):
        query = (
            db.query(Order)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.food),          
                joinedload(Order.customer),
                joinedload(Order.driver),
                joinedload(Order.restaurant),
                joinedload(Order.address)            
            )
            .filter(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
        )
        total = query.count()
        orders = query.offset((page - 1) * limit).limit(limit).all()
        return orders, total

    def get_all_with_items(self, db: Session, page: int = 1, limit: int = 10):
        query = (
            db.query(Order)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.food),
                joinedload(Order.customer),
                joinedload(Order.driver),
                joinedload(Order.restaurant),
                joinedload(Order.address)
            )
            .order_by(Order.created_at.desc())
        )
        total = query.count()
        orders = query.offset((page - 1) * limit).limit(limit).all()
        return orders, total

    def update_order(self, db: Session, uid: UUID, order_in: OrderUpdate) -> Order:
        order = self.get_record_by_field(db, "uid", uid)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order_in.status and order_in.status != order.status:
            allowed = ORDER_STATUS_FLOW.get(order.status.lower(), set())
            if order_in.status.lower() not in allowed:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid status transition: {order.status} → {order_in.status}",
                )

        if order_in.subtotal is not None:
            order.subtotal = order_in.subtotal
        if order_in.delivery_fee is not None:
            order.delivery_fee = order_in.delivery_fee
        if order_in.subtotal is not None or order_in.delivery_fee is not None:
            order.total = order.subtotal + order.delivery_fee
        if order_in.status is not None:
            order.status = order_in.status.lower()

            # ── Auto set driver available when delivered ───────────────────────────
            if order_in.status.lower() == "delivered" and order.driver_id:
                from app.models.driver import Driver
                driver = (
                    db.query(Driver)
                    .filter(Driver.user_id == order.driver_id)  # ← order.driver_id is user.id
                    .first()
                )
                if driver:
                    driver.status = "available"
                    db.add(driver)

        db.commit()
        db.refresh(order)
        return order

    def delete_order(self, db: Session, uid: UUID):
        order = self.get_record_by_field(db, "uid", uid)
        if order.status not in {"pending", "cancelled"}:
            raise HTTPException(
                status_code=400,
                detail="Only pending or cancelled orders can be deleted",
            )
        db.delete(order)
        db.commit()
        return {"detail": "Order deleted successfully"}


crud_order = CRUDOrder(MODEL)