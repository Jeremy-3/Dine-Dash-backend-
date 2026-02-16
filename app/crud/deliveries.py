from app.models.deliveries import Delivery
from app.models.driver import Driver
from app.schemas.deliveries import DeliveryCreate, DeliveryUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime
from app.schemas.constants import DELIVERY_STATUSES

MODEL = Delivery

ALLOWED_DELIVERY_TRANSITIONS = {
    "pending": ["assigned"],
    "assigned": ["picked_up"],
    "picked_up": ["delivered"],
}

class CRUDDelivery(CRUDBase[MODEL]):
    def create_delivery(self, db: Session, record_create: DeliveryCreate):
        # Ensure one delivery per order
        existing = self.get_record_by_field(db, "order_id", record_create.order_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery already exists for this order"
            )

        delivery = self.create(db, record_create)
        return delivery


    def assign_driver(self, db: Session, uid: UUID, driver_id: int):
            delivery = self.get_record_by_field(db, "uid", uid)
            if not delivery:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Delivery not found"
                )
            

            if delivery.status != "pending":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Driver can only be assigned to pending deliveries"
                )

            driver = db.query(Driver).filter(Driver.id == driver_id).first()
            if not driver:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Driver not found"
                )

            if driver.status != "available":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Driver is not available"
                )

            delivery.driver_id = driver_id
            delivery.status = "assigned"
            db.commit()
            db.refresh(delivery)

            return delivery

    def update_delivery(self, db: Session, uid: UUID, record_in: DeliveryUpdate):
        delivery = self.get_delivery_by_uid(db, uid)

        # Validate status transitions
        if record_in.status:
            allowed = ALLOWED_DELIVERY_TRANSITIONS.get(delivery.status, [])
            if record_in.status not in allowed:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status transition from {delivery.status} to {record_in.status}"
                )

            # Handle timestamps
            if record_in.status == "picked_up":
                delivery.picked_up_at = datetime.utcnow()
            elif record_in.status == "delivered":
                delivery.delivered_at = datetime.utcnow()

        updated_delivery = self.update(db, delivery, record_in)
        return updated_delivery

    def delete_delivery(self, db: Session, uid: UUID):
        delivery = self.get_delivery_by_uid(db, uid)

        if delivery.status in ["picked_up", "delivered"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete delivery already in progress or completed"
            )

        db.delete(delivery)
        db.commit()





crud_delivery = CRUDDelivery(MODEL)