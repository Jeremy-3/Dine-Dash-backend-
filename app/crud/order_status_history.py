from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from app.models.order_status_history import OrderStatusHistory
from app.models.order import Order
from app.schemas.order_status_history import OrderStatusHistoryCreate
from app.schemas.constants import ORDER_STATUSES
from app.crud.base import CRUDBase

MODEL = OrderStatusHistory


class CRUDOrderStatusHistory(CRUDBase[MODEL]):
    """Append-only CRUD for OrderStatusHistory"""

    # -------------------------
    # CREATE (internal use only)
    # -------------------------
    def log_status_change(
        self,
        db: Session,
        order_id: int,
        new_status: str,
    ) -> OrderStatusHistory:
        if new_status not in ORDER_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid order status",
            )

        history = MODEL(
            order_id=order_id,
            status=new_status,
        )

        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    # -------------------------
    # READ: order timeline
    # -------------------------
    def get_order_history(
        self,
        db: Session,
        order_id: int,
    ):
        return (
            db.query(MODEL)
            .filter(MODEL.order_id == order_id)
            .order_by(MODEL.created_at.asc())
            .all()
        )


crud_order_status_history = CRUDOrderStatusHistory(MODEL)
