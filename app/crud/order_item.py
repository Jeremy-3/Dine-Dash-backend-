from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from uuid import UUID
from app.models.order_item import OrderItem
from app.models.order import Order
from app.models.foods import Food
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate
# from app.schemas.constants import ORDER_STATUSES
from app.crud.base import CRUDBase

NON_EDITABLE_STATUSES = {
    "CONFIRMED",
    "preparing",
    "in_transit",
    "DELIVERED",
    "CANCELLED",
}

MODEL = OrderItem


class CRUDOrderItem(CRUDBase[MODEL]):
    """CRUD operations for OrderItem"""

    # Helpers
    def _get_order(self, db: Session, order_id: int) -> Order:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return order

    def _ensure_order_editable(self, order: Order):
        if order.status in NON_EDITABLE_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Order cannot be modified in status '{order.status}'",
            )

    def add_item(self,db: Session,item_in: OrderItemCreate):
        order = self._get_order(db, item_in.order_id)
        self._ensure_order_editable(order)

        food = db.query(Food).filter(Food.id == item_in.food_id).first()
        if not food:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food item not found",
            )

        item = OrderItem(
            order_id=order.id,
            food_id=food.id,
            quantity=item_in.quantity,
            price_at_order=food.price,  # snapshot price
        )

        db.add(item)
        db.flush()

        self._recalculate_order_totals(db, order)

        db.commit()
        db.refresh(item)
        return item

    def get_items_by_order(self,db: Session,order_id: int):
        return (
            db.query(MODEL)
            .options(joinedload(MODEL.food))
            .filter(MODEL.order_id == order_id)
            .all()
        )

    def update_item(self,db: Session,item_id: int,item_in: OrderItemUpdate):
        item = db.query(MODEL).filter(MODEL.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order item not found",
            )

        order = self._get_order(db, item.order_id)
        self._ensure_order_editable(order)

        if item_in.quantity is not None:
            item.quantity = item_in.quantity

        if item_in.price_at_order is not None:
            item.price_at_order = item_in.price_at_order

        self._recalculate_order_totals(db, order)

        db.commit()
        db.refresh(item)
        return item

    def remove_item(self,db: Session,item_id: int):
        item = db.query(MODEL).filter(MODEL.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order item not found",
            )

        order = self._get_order(db, item.order_id)
        self._ensure_order_editable(order)

        db.delete(item)
        db.flush()

        self._recalculate_order_totals(db, order)

        db.commit()
        return {"detail": "Order item removed"}


    def _recalculate_order_totals(self, db: Session, order: Order):
        items = (
            db.query(MODEL)
            .filter(MODEL.order_id == order.id)
            .all()
        )

        subtotal = sum(
            (item.quantity * item.price_at_order) for item in items
        )

        order.subtotal = subtotal
        order.total = subtotal + order.delivery_fee
        db.add(order)
