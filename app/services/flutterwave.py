import httpx
import hashlib
import hmac
from app.core.config import settings
from app.utils.logger import logger


def get_headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
        "Content-Type":  "application/json",
    }


def initiate_payment(
    order_id:    int,
    amount:      float,
    currency:    str,
    email:       str,
    phone:       str,
    name:        str,
    tx_ref:      str,   
) -> dict:
    """
    Create a hosted payment link — customer is redirected to
    Flutterwave's secure page to enter card details.
    Returns a payment link URL.
    """
    payload = {
        "tx_ref":          tx_ref,
        "amount":          amount,
        "currency":        currency,    # "KES"
        "redirect_url":    settings.FLW_REDIRECT_URL,
        "customer": {
            "email":        email,
            "phone_number": phone,
            "name":         name,
        },
        "customizations": {
            "title":       "Dine & Dash",
            "description": f"Payment for order {tx_ref}",
            # "logo":        "https://your-logo-url.com/logo.png",
        },
        "meta": {
            "order_id": order_id,       # passed back in webhook + redirect
        },
    }

    logger.info("=" * 60)
    logger.info("FLUTTERWAVE PAYMENT INITIATION")
    logger.info(f"  tx_ref:   {tx_ref}")
    logger.info(f"  amount:   {amount} {currency}")
    logger.info(f"  email:    {email}")
    logger.info(f"  order_id: {order_id}")
    logger.info("=" * 60)

    response = httpx.post(
        f"{settings.FLW_BASE_URL}/payments",
        json=payload,
        headers=get_headers(),
        timeout=30,
    )

    logger.info(f"Flutterwave response: {response.status_code} — {response.text}")
    response.raise_for_status()

    data = response.json()
    return {
        "payment_link": data["data"]["link"],
        "tx_ref":       tx_ref,
    }


def verify_transaction(transaction_id: str) -> dict:
    """
    Verify a completed transaction by Flutterwave transaction ID.
    Call this after redirect or webhook to confirm payment.
    """
    logger.info(f"Verifying Flutterwave transaction: {transaction_id}")

    response = httpx.get(
        f"{settings.FLW_BASE_URL}/transactions/{transaction_id}/verify",
        headers=get_headers(),
        timeout=30,
    )

    logger.info(f"Verify response: {response.status_code} — {response.text}")
    response.raise_for_status()

    data = response.json()
    return data["data"]


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify that the webhook came from Flutterwave and not someone else.
    Flutterwave sends a 'verif-hash' header — compare with your secret hash.
    """
    expected = settings.FLW_SECRET_KEY   # Flutterwave uses secret key as hash
    return hmac.compare_digest(signature, expected)