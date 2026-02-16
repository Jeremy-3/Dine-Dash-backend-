from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate
from app.schemas.constants import ORDER_STATUSES
from app.crud.base import CRUDBase

MODEL = Order


# Optional but recommended: allowed transitions
ORDER_STATUS_FLOW = {
    "PENDING": {"CONFIRMED", "CANCELLED"},
    "CONFIRMED": {"PREPARING", "CANCELLED"},
    "PREPARING": {"OUT_FOR_DELIVERY"},
    "OUT_FOR_DELIVERY": {"DELIVERED"},
    "DELIVERED": set(),
    "CANCELLED": set(),
}


class CRUDOrder(CRUDBase[MODEL]):
    """CRUD operations for Order model"""
    def create_order(self, db: Session, order_in: OrderCreate) -> Order:
        total = order_in.subtotal + order_in.delivery_fee

        new_order = MODEL(
            customer_id=order_in.customer_id,
            status=order_in.status,
            subtotal=order_in.subtotal,
            delivery_fee=order_in.delivery_fee,
            total=total,
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order



    def list_orders( self, db: Session, page: int = 1, limit: int = 10, customer_id: int | None = None):
        conditions = []
        if customer_id:
            conditions.append({"field": "customer_id", "value": customer_id})

        return self.read_records(
            db=db,
            page=page,
            limit=limit,
            conditions=conditions,
        )

    def update_order(self, db: Session, uid: UUID,order_in: OrderUpdate) -> Order:
        order = self.get_record_by_field(db, "uid", uid)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        # Validate status transition
        if order_in.status and order_in.status != order.status:
            allowed = ORDER_STATUS_FLOW.get(order.status, set())
            if order_in.status not in allowed:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status transition: {order.status} → {order_in.status}",
                )

        # Apply updates
        if order_in.subtotal is not None:
            order.subtotal = order_in.subtotal

        if order_in.delivery_fee is not None:
            order.delivery_fee = order_in.delivery_fee

        # Recalculate total if needed
        if order_in.subtotal is not None or order_in.delivery_fee is not None:
            order.total = order.subtotal + order.delivery_fee

        if order_in.status is not None:
            order.status = order_in.status

        db.commit()
        db.refresh(order)
        return order


    def delete_order(self, db: Session, uid: UUID):
        order = self.get_by_uid(db, uid)

        if order.status not in {"PENDING", "CANCELLED"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending or cancelled orders can be deleted",
            )

        db.delete(order)
        db.commit()
        return {"detail": "Order deleted successfully"}


crud_order = CRUDOrder(MODEL)
