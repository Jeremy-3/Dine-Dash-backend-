import base64
import httpx
from datetime import datetime
from app.core.config import settings
from app.utils.logger import logger


def get_access_token() -> str:
    credentials = base64.b64encode(
        f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode()
    ).decode()

    logger.info(f"Requesting M-Pesa access token from {settings.MPESA_BASE_URL}")

    response = httpx.get(
        f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {credentials}"},
        timeout=30,
    )

    logger.info(f"Token response: {response.status_code} — {response.text}")
    response.raise_for_status()
    return response.json()["access_token"]


def get_password() -> tuple[str, str]:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    raw       = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    password  = base64.b64encode(raw.encode()).decode()
    return password, timestamp


def stk_push(phone: str, amount: int, order_id: int, description: str = "Food order payment") -> dict:
    # Normalize phone
    phone = phone.lstrip("+")
    if phone.startswith("0"):
        phone = "254" + phone[1:]

    token             = get_access_token()
    password, timestamp = get_password()

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password":          password,
        "Timestamp":         timestamp,
        "TransactionType":   "CustomerPayBillOnline",
        "Amount":            amount,
        "PartyA":            phone,
        "PartyB":            settings.MPESA_SHORTCODE,
        "PhoneNumber":       phone,
        "CallBackURL":       settings.MPESA_CALLBACK_URL,
        "AccountReference":  f"DineDash #{order_id}",
        "TransactionDesc":   f"{description[:20]}...",
    }

    # ── Log everything going to Safaricom ──────────────────────────────────
    logger.info("=" * 60)
    logger.info("STK PUSH REQUEST")
    logger.info(f"  URL:           {settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest")
    logger.info(f"  ENV:           {settings.MPESA_ENV}")
    logger.info(f"  Shortcode:     {settings.MPESA_SHORTCODE}")
    logger.info(f"  Phone:         {phone}")
    logger.info(f"  Amount:        {amount}")
    logger.info(f"  CallbackURL:   {settings.MPESA_CALLBACK_URL}")
    logger.info(f"  OrderRef:      ORDER-{order_id}")
    logger.info(f"  Timestamp:     {timestamp}")
    # Don't log full password — just confirm it was generated
    logger.info(f"  Password set:  {'yes' if password else 'NO — EMPTY!'}")
    logger.info("=" * 60)

    response = httpx.post(
        f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/json",
        },
        timeout=30,
    )

    # ── Log Safaricom's full response ──────────────────────────────────────
    logger.info("STK PUSH RESPONSE")
    logger.info(f"  Status:  {response.status_code}")
    logger.info(f"  Body:    {response.text}")
    logger.info("=" * 60)

    response.raise_for_status()
    return response.json()


def query_stk_status(checkout_request_id: str) -> dict:
    token             = get_access_token()
    password, timestamp = get_password()

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password":          password,
        "Timestamp":         timestamp,
        "CheckoutRequestID": checkout_request_id,
    }

    logger.info(f"Querying STK status for: {checkout_request_id}")

    response = httpx.post(
        f"{settings.MPESA_BASE_URL}/mpesa/stkpushquery/v1/query",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )

    logger.info(f"STK status response: {response.status_code} — {response.text}")
    response.raise_for_status()
    return response.json()