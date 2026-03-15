from app.crud.payments import crud_payment
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentOut  # ← add PaymentOut
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post(
    "/",
    response_model=ResponseModel[PaymentOut],
    dependencies=[Depends(require_permission("payment.process"))]
)
def create_payment(payment_create: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = crud_payment.create_payment(db, payment_create)
    return ResponseModel(
        data=PaymentOut.model_validate(new_payment),   # ← ORM → Pydantic
        message="Payment created successfully"
    )


@router.get(
    "/by-order/{order_uid}",
    response_model=ResponseModel[list[PaymentOut]],
    dependencies=[Depends(require_permission("payments.view_own"))]
)
def get_payments_by_order(order_uid: UUID, db: Session = Depends(get_db)):
    payments = crud_payment.get_payments_by_order(db, order_uid)
    return ResponseModel(
        data=[PaymentOut.model_validate(p) for p in payments],  # ← ORM → Pydantic
        message="Payments retrieved successfully"
    )


@router.get(
    "/",
    response_model=ResponseModel[list[PaymentOut]],
    dependencies=[Depends(require_permission("payments.view_all"))]
)
def get_all_payments(db: Session = Depends(get_db)):
    payments, total = crud_payment.read(db)
    return ResponseModel(
        data=[PaymentOut.model_validate(p) for p in payments],  # ← ORM → Pydantic
        message="Payments retrieved successfully",
        total=total
    )


@router.get(
    "/{uid}",
    response_model=ResponseModel[PaymentOut],
    dependencies=[Depends(require_permission("payments.view_own"))]
)
def get_payment(uid: UUID, db: Session = Depends(get_db)):
    payment = crud_payment.get_record_by_field(db, "uid", uid)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return ResponseModel(
        data=PaymentOut.model_validate(payment),       # ← ORM → Pydantic
        message="Payment retrieved successfully"
    )


@router.put(
    "/{uid}",
    response_model=ResponseModel[PaymentOut],
    dependencies=[Depends(require_permission("payments.view_all"))]
)
def update_payment(uid: UUID, payment_update: PaymentUpdate, db: Session = Depends(get_db)):
    payment = crud_payment.get_record_by_field(db, "uid", uid)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    updated_payment = crud_payment.update_payment(db, payment.id, payment_update)
    return ResponseModel(
        data=PaymentOut.model_validate(updated_payment),  # ← ORM → Pydantic
        message="Payment updated successfully"
    )