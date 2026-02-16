from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.crud.base import CRUDBase
from app.schemas.constants import PAYMENT_STATUSES


MODEL = Payment

class CRUDPayment(CRUDBase[MODEL]):
    """CRUD operations for Payment model"""

    def create_payment(self,db: Session,payment_in: PaymentCreate,):
        """Create a new payment.  """

        # prevent multiple payments per order
        existing_payment = self.get_record_by_field(
            db, "order_id", payment_in.order_id
        )
        if existing_payment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment already exists for this order",
            )

        record_data = payment_in.model_dump()
        record_data["paid_at"] = datetime.utcnow() if record_data["status"] == "PAID" else None 

        new_payment = self.create(db, PaymentCreate(**record_data))

        return new_payment


    def update_payment( self,db: Session,payment_id: int, payment_in: PaymentUpdate,):
        """
        Update payment (partial update).
        """

        payment = self.get(db, payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found",
            )

        # Prevent modification if already paid
        if payment.status == "PAID":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Paid payments cannot be modified",
            )

        update_data = payment_in.model_dump(exclude_unset=True)

        # Handle paid_at automatically
        if update_data.get("status") == "PAID":
            update_data["paid_at"] = datetime.utcnow()

        for field, value in update_data.items():
            setattr(payment, field, value)

        db.commit()
        db.refresh(payment)
        return payment

    def get_payment_by_order(self,db: Session, order_id: int):
        """
        Fetch payment by order ID.
        """
        return self.get_record_by_field(db, "order_id", order_id)

    def delete_payment(self,db: Session, payment_id: int):
        """
        Delete payment (use with caution).
        """
        payment = self.get(db, payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found",
            )

        db.delete(payment)
        db.commit()


crud_payment = CRUDPayment(MODEL)
