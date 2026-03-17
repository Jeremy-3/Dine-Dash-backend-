from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import mpesa as mpesa_service
from app.models.payment import Payment
from app.schemas.response import ResponseModel
from app.dependencies.rbac import require_permission
from app.dependencies.auth import get_current_user
from app.models.user import User
from pydantic import BaseModel
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/payments/mpesa", tags=["mpesa"])


class STKPushRequest(BaseModel):
    order_id: int
    amount:   int       
    phone:    str       


class STKStatusRequest(BaseModel):
    checkout_request_id: str


@router.post("/stk-push", response_model=ResponseModel,
             dependencies=[Depends(require_permission("payments.process"))])
def initiate_stk_push(
    body: STKPushRequest,
    db:   Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        result = mpesa_service.stk_push(
            phone=body.phone,
            amount=body.amount,
            order_id=body.order_id,
        )
    except Exception as e:
        logger.error(f"STK push failed: {e}")
        raise HTTPException(status_code=502, detail="M-Pesa request failed. Try again.")

    checkout_id = result.get("CheckoutRequestID")

    # ── Check if a payment already exists for this order ──────────────────
    existing = db.query(Payment).filter(Payment.order_id == body.order_id).first()

    if existing:
        # Update the existing record with the new checkout_request_id
        existing.checkout_request_id = checkout_id
        existing.status  = "pending"
        existing.phone   = body.phone
        existing.paid_at = None
        existing.mpesa_receipt = None
        db.commit()
        logger.info(f"Updated existing payment record for order {body.order_id}")
    else:
        # Create new payment record
        payment = Payment(
            order_id=body.order_id,
            amount=body.amount,
            method="mpesa",
            status="pending",
            phone=body.phone,
            checkout_request_id=checkout_id,
            paid_at=None
        )
        db.add(payment)
        db.commit()
        logger.info(f"Created new payment record for order {body.order_id}")

    return ResponseModel(
        data={"checkout_request_id": checkout_id},
        message="STK push sent. Ask customer to check their phone."
    )


@router.post("/callback")
async def mpesa_callback(request: Request, db: Session = Depends(get_db)):
    """
    Safaricom calls this URL after customer completes or cancels payment.
    This endpoint must be PUBLIC — no auth required.
    """
    body = await request.json()
    logger.info(f"M-Pesa callback received: {body}")

    try:
        stk_callback = body["Body"]["stkCallback"]
        checkout_id  = stk_callback["CheckoutRequestID"]
        result_code  = stk_callback["ResultCode"]  # 0 = success

        # Find the matching payment
        payment = db.query(Payment).filter(
            Payment.checkout_request_id == checkout_id
        ).first()

        if not payment:
            logger.warning(f"No payment found for CheckoutRequestID: {checkout_id}")
            return {"ResultCode": 0, "ResultDesc": "Accepted"}

        if result_code == 0:
            # Success — extract receipt from metadata
            items = stk_callback.get("CallbackMetadata", {}).get("Item", [])
            receipt = next((i["Value"] for i in items if i["Name"] == "MpesaReceiptNumber"), None)

            payment.status       = "success"
            payment.mpesa_receipt = receipt
            payment.paid_at      = datetime.now(timezone.utc)
        else:
            # Failed or cancelled
            payment.status = "failed"

        db.commit()

    except Exception as e:
        logger.error(f"Callback processing error: {e}")

    # Always return success to Safaricom — even on our errors
    # If you return an error, Safaricom will retry the callback
    return {"ResultCode": 0, "ResultDesc": "Accepted"}


@router.get(
    "/status/{checkout_request_id}",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("payments.view_own"))]
)
def get_payment_status(checkout_request_id: str, db: Session = Depends(get_db)):
    """Poll payment status — frontend calls this every 3 seconds after STK push."""
    payment = db.query(Payment).filter(
        Payment.checkout_request_id == checkout_request_id
    ).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return ResponseModel(
        data={
            "status":        payment.status,
            "mpesa_receipt": payment.mpesa_receipt,
            "amount":        float(payment.amount),
            "paid_at":       payment.paid_at.isoformat() if payment.paid_at else None,
        },
        message="Payment status retrieved"
    )