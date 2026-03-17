from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import flutterwave as flw_service
from app.models.payment import Payment
from app.models.order import Order
from app.schemas.response import ResponseModel
from app.dependencies.rbac import require_permission
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.utils.logger import logger
from pydantic import BaseModel
from datetime import datetime, timezone
import time

router = APIRouter(prefix="/payments/card", tags=["card-payments"])


class CardPaymentRequest(BaseModel):
    order_id: int
    amount:   float
    currency: str = "KES"   # default to KES


@router.post(
    "/initiate",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("payments.process"))]
)
def initiate_card_payment(
    body:         CardPaymentRequest,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Creates a Flutterwave payment link.
    Frontend opens this link in a new tab or redirects to it.
    """
    # Generate a unique transaction reference
    tx_ref = f"ORDER-{body.order_id}-{int(time.time())}"

    try:
        result = flw_service.initiate_payment(
            order_id = body.order_id,
            amount   = body.amount,
            currency = body.currency,
            email    = current_user.email,
            phone    = current_user.phone or "",
            name     = current_user.name,
            tx_ref   = tx_ref,
        )
    except Exception as e:
        logger.error(f"Flutterwave initiation failed: {e}")
        raise HTTPException(status_code=502, detail="Card payment initiation failed.")

    # Save pending payment record
    existing = db.query(Payment).filter(Payment.order_id == body.order_id).first()
    if existing:
        existing.method   = "card"
        existing.status   = "pending"
        existing.tx_ref   = tx_ref
        existing.paid_at  = None
        db.commit()
    else:
        payment = Payment(
            order_id = body.order_id,
            amount   = body.amount,
            method   = "card",
            status   = "pending",
            tx_ref   = tx_ref,
        )
        db.add(payment)
        db.commit()

    return ResponseModel(
        data={"payment_link": result["payment_link"], "tx_ref": tx_ref},
        message="Payment link created successfully."
    )


@router.get("/verify")
def verify_card_payment(
    status:         str   = Query(...),
    tx_ref:         str   = Query(...),
    transaction_id: str   = Query(...),
    db:             Session = Depends(get_db),
):
    """
    Flutterwave redirects customer here after payment.
    Verifies the transaction and updates payment status.
    Then redirects customer to their orders page.
    """
    logger.info(f"Card payment redirect — status: {status}, tx_ref: {tx_ref}, id: {transaction_id}")

    payment = db.query(Payment).filter(Payment.tx_ref == tx_ref).first()

    if not payment:
        logger.warning(f"No payment found for tx_ref: {tx_ref}")
        return RedirectResponse(url="/customer?payment=not_found")

    if status == "successful":
        try:
            # Double-check with Flutterwave API
            verified = flw_service.verify_transaction(transaction_id)
            if verified["status"] == "successful" and float(verified["amount"]) >= float(payment.amount):
                payment.status       = "success"
                payment.paid_at      = datetime.now(timezone.utc)
                payment.flw_tx_id    = transaction_id
                db.commit()
                logger.info(f"Card payment verified: {tx_ref}")
                return RedirectResponse(url="/customer?payment=success")
            else:
                payment.status = "failed"
                db.commit()
                return RedirectResponse(url="/customer?payment=failed")
        except Exception as e:
            logger.error(f"Verification error: {e}")
            payment.status = "failed"
            db.commit()
            return RedirectResponse(url="/customer?payment=failed")
    else:
        payment.status = "failed"
        db.commit()
        return RedirectResponse(url="/customer?payment=failed")


@router.post("/webhook")
async def flutterwave_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Flutterwave sends payment events here.
    This is the server-side confirmation — more reliable than redirect.
    Must be PUBLIC — no auth.
    """
    # Verify the webhook signature
    signature = request.headers.get("verif-hash", "")
    if not flw_service.verify_webhook_signature(
        await request.body(), signature
    ):
        logger.warning("Invalid Flutterwave webhook signature")
        raise HTTPException(status_code=401, detail="Invalid signature")

    body = await request.json()
    logger.info(f"Flutterwave webhook: {body}")

    event = body.get("event")
    data  = body.get("data", {})

    if event == "charge.completed" and data.get("status") == "successful":
        tx_ref = data.get("tx_ref", "")
        payment = db.query(Payment).filter(Payment.tx_ref == tx_ref).first()

        if payment:
            payment.status    = "success"
            payment.paid_at   = datetime.now(timezone.utc)
            payment.flw_tx_id = str(data.get("id", ""))
            db.commit()
            logger.info(f"Webhook: payment confirmed for tx_ref {tx_ref}")

    return {"status": "ok"}