# Dine & Dash — Backend API

> FastAPI + PostgreSQL + SQLAlchemy REST API powering the Dine & Dash food delivery platform.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Environment Variables](#environment-variables)
- [Database Setup & Migrations](#database-setup--migrations)
- [Running the Server](#running-the-server)
- [API Reference](#api-reference)
- [Payment Integration](#payment-integration)
- [Deployment (Render)](#deployment-render)

---

## Architecture Overview

```
React Frontend (Vercel)
        │
        │  HTTPS requests to /api/*
        ▼
FastAPI Backend (Render)
        │
        ├── JWT Auth (python-jose)
        ├── RBAC (role + permission system)
        ├── SQLAlchemy ORM
        │
        ├── PostgreSQL Database
        │
        ├── Safaricom Daraja API (M-Pesa STK Push)
        └── Flutterwave API (Card Payments)
```

The frontend never calls the database directly. All data flows through the FastAPI REST API, which enforces authentication and permission checks on every protected endpoint.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.110.0 |
| ORM | SQLAlchemy 2.0.25 |
| Database | PostgreSQL (psycopg2-binary 2.9.9) |
| Migrations | Alembic 1.13.1 |
| Auth | python-jose 3.3.0 (JWT), bcrypt 5.0.0 |
| Validation | Pydantic 2.6.4 |
| HTTP Client | httpx 0.27.0 (M-Pesa + Flutterwave) |
| Server | Uvicorn 0.29.0 |
| Payments | Safaricom Daraja API, Flutterwave v3 |

---

## Project Structure

```
dine-dash-backend/
├── app/
│   ├── main.py                  # FastAPI app, middleware, router registration
│   ├── core/
│   │   ├── config.py            # Settings (reads from .env)
│   │   ├── constants.py         # Seed data, role IDs, default permissions
│   │   └── security.py          # Password hashing, JWT creation/verification
│   ├── db/
│   │   ├── base.py              # SQLAlchemy declarative base
│   │   └── session.py           # DB session factory, get_db dependency
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── driver.py
│   │   ├── deliveries.py
│   │   ├── address.py
│   │   ├── payment.py
│   │   ├── restaurants.py
│   │   ├── food.py
│   │   ├── combo.py
│   │   ├── combo_item.py
│   │   ├── roles.py
│   │   ├── permissions.py
│   │   └── role_permission.py
│   ├── schemas/                 # Pydantic request/response models
│   │   ├── user.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   ├── combo.py
│   │   └── ...
│   ├── crud/                    # Database CRUD operations
│   │   ├── base.py              # Generic CRUDBase class
│   │   ├── user.py
│   │   ├── orders.py
│   │   └── ...
│   ├── routes/                  # FastAPI route handlers
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── orders.py
│   │   ├── payments.py
│   │   ├── mpesa.py
│   │   ├── card.py
│   │   └── ...
│   ├── dependencies/
│   │   ├── auth.py              # get_current_user dependency
│   │   └── rbac.py              # require_permission dependency
│   ├── services/
│   │   ├── mpesa.py             # Safaricom Daraja API integration
│   │   └── flutterwave.py       # Flutterwave card payment integration
│   ├── handlers/
│   │   └── exception_handlers.py
│   └── utils/
│       ├── logger.py
│       └── validate.py          # Phone number validation
├── alembic/
│   ├── env.py
│   └── versions/               # Migration files
├── alembic.ini
├── requirements.txt
└── .env
```

---

## Local Development Setup

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Git

### 1. Clone and create virtual environment

```bash
git clone https://github.com/yourname/dine-dash-backend.git
cd dine-dash-backend

python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your database

```bash
psql -U postgres
CREATE DATABASE dine_dash;
\q
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your values 
```

### 5. Run migrations and seed data

```bash
alembic upgrade head
```

If you have a seed command:

```bash
python -m app.commands.seed_all       
```

### 6. Start the development server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`


---

## Environment Variables

Create a `.env` file in the root directory. All variables are required unless marked optional.

```env
# ── Application ────────────────────────────────────────────────────────────────
APP_ENV=development                         # development | production
DEBUG=true                                  # true | false

# ── Database ───────────────────────────────────────────────────────────────────
DATABASE_URL=postgresql://user:pass@localhost:5432/dine_dash

# ── JWT Authentication ─────────────────────────────────────────────────────────
JWT_SECRET_KEY=your-very-secret-key-here    # Use a long random string in production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_SECONDS=14400           # 4 hours
OTP_TOKEN_EXPIRE_SECONDS=300                # 5 minutes

# ── Superadmin (seeded on first run) ───────────────────────────────────────────
SUPERADMIN_NAME=Superadmin
SUPERADMIN_EMAIL=superadmin@yourdomain.com
SUPERADMIN_PHONE=+254700000000
SUPERADMIN_PASSWORD=YourStrongPassword!

# ── M-Pesa (Safaricom Daraja) ──────────────────────────────────────────────────
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379                      # Sandbox: 174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919   # Sandbox passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/payments/mpesa/callback
MPESA_ENV=sandbox                           # sandbox | production

# ── Flutterwave (Card Payments) ────────────────────────────────────────────────
FLW_PUBLIC_KEY=FLWPUBK_TEST-xxxxxxxxxxxx
FLW_SECRET_KEY=FLWSECK_TEST-xxxxxxxxxxxx
FLW_ENCRYPTION_KEY=your_32_char_key
FLW_CALLBACK_URL=https://yourdomain.com/api/payments/card/callback
FLW_REDIRECT_URL=https://yourdomain.com/api/payments/card/verify
FLW_ENV=test                                # test | production

# ── Email (optional) ───────────────────────────────────────────────────────────
MAIL_FROM=noreply@yourdomain.com
```

### Role IDs (built into constants.py)

| Role | ID |
|---|---|
| Superadmin | 1 |
| Admin | 2 |
| Manager | 3 |
| Driver | 4 |
| Customer | 5 |

---

## Database Setup & Migrations

This project uses Alembic for database migrations.

### Create a new migration after model changes

```bash
alembic revision --autogenerate -m "describe your change"
```

### Apply all pending migrations

```bash
alembic upgrade head
```

### Roll back one migration

```bash
alembic downgrade -1
```

### View migration history

```bash
alembic history --verbose
```

### Database schema overview

```
roles ──────────────────────────────────────────────────────┐
  id, uid, name, active                                      │
                                                             │
permissions ────────────────────────────────────────────────┤
  id, uid, name, description, category                       │
                                                             │
role_permissions ───────────────────────────────────────────┤
  role_id (FK roles), permission_id (FK permissions)         │
                                                             │
users ──────────────────────────────────────────────────────┤
  id, uid, name, email, phone, password_hash                 │
  role_id (FK roles), is_active                              │
       │                                                     │
       ├── drivers ──────────────────────────────────────────┤
       │     id, uid, user_id (FK users), status             │
       │                                                     │
       └── orders ───────────────────────────────────────────┤
             id, uid, customer_id (FK users)                 │
             driver_id (FK users), restaurant_id             │
             status, subtotal, delivery_fee, total           │
              │                                              │
              ├── order_items                                │
              │     id, order_id, food_id, name              │
              │     quantity, price_at_order                  │
              │                                              │
              ├── addresses                                  │
              │     id, uid, order_id, street                │
              │     city, state, zip_code, notes             │
              │                                              │
              ├── payments                                   │
              │     id, uid, order_id, amount, method        │
              │     status, phone, checkout_request_id       │
              │     mpesa_receipt, tx_ref, flw_tx_id         │
              │                                              │
              └── deliveries                                 │
                    id, uid, order_id, driver_id             │
                    restaurant_id, assigned_by               │
                    status, assigned_at, delivered_at        │
                                                             │
restaurants ────────────────────────────────────────────────┤
  id, uid, name, street, city, state, zip_code, phone        │
                                                             │
foods ──────────────────────────────────────────────────────┤
  id, uid, name, description, category, price, available     │
                                                             │
combos ─────────────────────────────────────────────────────┤
  id, uid, name, description, combo_price, is_available      │
       │                                                     │
       └── combo_items                                       │
             id, combo_id (FK combos), food_id (FK foods)   │
             quantity                                        │
```

---

## Running the Server

### Development (with auto-reload)

```bash
uvicorn app.main:app --reload --port 8000
```

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## API Reference

All endpoints are prefixed with `/api`. Protected endpoints require a Bearer token in the Authorization header.

```
Authorization: Bearer <access_token>
```

### Standard response shape

```json
{
  "success": true,
  "data": {},
  "message": "Operation successful",
  "errors": null,
  "total": null
}
```

---

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/login` | Public | Login, returns JWT token |
| POST | `/api/auth/signup` | Public | Register new user |
| GET | `/api/auth/me` | Required | Get current user profile |

**POST /api/auth/login**
```json
// Request
{ "email": "user@example.com", "password": "password123" }

// Response
{
  "data": {
    "access_token": "eyJ...",
    "user": {
      "id": 7, "uid": "uuid", "name": "John Kariuki",
      "email": "customer@demo.com", "phone": "+254711000001",
      "role_id": 5, "role": { "id": 5, "name": "customer" }
    }
  }
}
```

**POST /api/auth/signup**
```json
// Request
{ "name": "John Kariuki", "email": "john@example.com", "password": "Pass123!", "role_id": 5 }
```

---

### Users

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/users/` | users.view_all | List all users (paginated) |
| POST | `/api/users/` | users.create | Create a user |
| GET | `/api/users/:uid` | users.view | Get user by UID |
| PUT | `/api/users/:uid` | users.edit | Update user |
| POST | `/api/users/apply-driver-role/:uid` | users.edit | Promote user to driver |

---

### Orders

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/orders/` | orders.view_all | List all orders |
| POST | `/api/orders/` | orders.create | Create order |
| GET | `/api/orders/my-orders` | orders.view_own | Customer's own orders (JWT) |
| GET | `/api/orders/my-deliveries` | deliveries.view_own | Driver's deliveries (JWT) |
| GET | `/api/orders/:uid` | orders.view_all | Get order by UID |
| PUT | `/api/orders/:uid` | orders.update_status | Update order status |
| POST | `/api/orders/:uid/assign` | deliveries.assign | Assign driver + restaurant |

**POST /api/orders/** (Create order — step 1 of 4)
```json
{ "customer_id": 7, "delivery_fee": 4.99 }
```

**POST /api/orders/:uid/assign**
```json
{ "driver_id": 2, "restaurant_id": 1 }
```

**Order status flow:**
```
pending → confirmed → assigned → picked_up → in_transit → delivered
                   ↘ cancelled
```

---

### Order Items

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| POST | `/api/order-items/bulk/add` | orders.create | Add items to order |
| GET | `/api/order-items/:order_id` | orders.view_own | Get items for order |
| DELETE | `/api/order-items/:id` | orders.edit | Remove item |

**POST /api/order-items/bulk/add**
```json
[
  { "order_id": 42, "food_id": 1, "quantity": 2 },
  { "order_id": 42, "food_id": 5, "quantity": 1 }
]
```

---

### Addresses

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| POST | `/api/addresses/` | addresses.create | Save delivery address |
| DELETE | `/api/addresses/:uid` | addresses.delete_own | Delete address |

**POST /api/addresses/** (step 3 of order creation)
```json
{
  "order_id": 42,
  "street": "Ngong Road",
  "city": "Nairobi",
  "state": "Nairobi County",
  "zip_code": "00200",
  "notes": "Gate code 1234"
}
```

---

### Payments

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| POST | `/api/payments/` | payments.process | Create payment record |
| GET | `/api/payments/` | payments.view_all | List all payments |
| GET | `/api/payments/by-order/:uid` | payments.view_own | Get payment for order |
| GET | `/api/payments/:uid` | payments.view_own | Get payment by UID |
| PUT | `/api/payments/:uid` | payments.view_all | Update payment |

---

### M-Pesa

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/payments/mpesa/stk-push` | Required | Initiate STK push |
| POST | `/api/payments/mpesa/callback` | **Public** | Safaricom callback |
| GET | `/api/payments/mpesa/status/:checkout_id` | Required | Poll payment status |

**POST /api/payments/mpesa/stk-push**
```json
{ "order_id": 42, "amount": 350, "phone": "254712345678" }
// Response
{ "data": { "checkout_request_id": "ws_CO_..." } }
```

**GET /api/payments/mpesa/status/:checkout_request_id**
```json
{
  "data": {
    "status": "success",
    "mpesa_receipt": "QHX73KDJLA",
    "amount": 350,
    "paid_at": "2026-03-17T14:32:00Z"
  }
}
```

---

### Card Payments (Flutterwave)

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/payments/card/initiate` | Required | Create Flutterwave payment link |
| GET | `/api/payments/card/verify` | **Public** | Flutterwave redirect handler |
| POST | `/api/payments/card/webhook` | **Public** | Flutterwave webhook |

**POST /api/payments/card/initiate**
```json
{ "order_id": 42, "amount": 350.50, "currency": "KES" }
// Response
{ "data": { "payment_link": "https://checkout.flutterwave.com/...", "tx_ref": "ORDER-42-1234567890" } }
```

---

### Foods

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/foods/` | foods.view | List foods (paginated) |
| POST | `/api/foods/` | foods.create | Create food item |
| GET | `/api/foods/:uid` | foods.view | Get food by UID |
| PUT | `/api/foods/:uid` | foods.edit | Update food |
| DELETE | `/api/foods/:uid` | foods.delete | Delete food |

---

### Combos

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/combos/available` | combos.view | List available combos |
| GET | `/api/combos/` | combos.view | List all combos |
| POST | `/api/combos/` | combos.create | Create combo |
| GET | `/api/combos/:uid` | combos.view | Get combo by UID |
| PUT | `/api/combos/:uid` | combos.edit | Update combo |
| DELETE | `/api/combos/:uid` | combos.delete | Delete combo |

**POST /api/combos/**
```json
{
  "name": "Burger Feast",
  "description": "Classic Cheeseburger + Fries + Drink",
  "combo_price": 15.99,
  "is_available": true,
  "items": [
    { "food_id": 1, "quantity": 1 },
    { "food_id": 22, "quantity": 1 }
  ]
}
```

---

### Restaurants

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/restaurants/` | restaurants.view | List restaurants (paginated) |
| POST | `/api/restaurants/` | restaurants.create | Create restaurant |
| GET | `/api/restaurants/:uid` | restaurants.view | Get restaurant by UID |
| PUT | `/api/restaurants/:uid` | restaurants.edit | Update restaurant |

---

### Drivers

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/drivers/` | drivers.view_all | List all drivers |
| POST | `/api/drivers/` | drivers.create | Create driver profile |
| GET | `/api/drivers/:uid` | drivers.view_all | Get driver by UID |
| PUT | `/api/drivers/:uid` | drivers.edit | Update driver status |
| DELETE | `/api/drivers/:uid` | drivers.delete | Deactivate driver |

---

### Roles & Permissions

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/roles/` | roles.view | List all roles |
| POST | `/api/roles/` | roles.create | Create role |
| PUT | `/api/roles/:uid` | roles.edit | Update role |
| GET | `/api/permissions/` | permissions.manage | List all permissions |
| POST | `/api/permissions/` | permissions.manage | Create permission |
| GET | `/api/role-permissions/:role_uid` | roles.view | Get role's permissions |
| POST | `/api/role-permissions/assign` | permissions.manage | Assign permission to role |
| POST | `/api/role-permissions/deassign` | permissions.manage | Remove permission from role |

---

### Deliveries

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/api/deliveries/` | deliveries.view_all | List all deliveries |
| POST | `/api/deliveries/` | deliveries.create | Create delivery record |
| GET | `/api/deliveries/:uid` | deliveries.view_all | Get delivery by UID |
| PUT | `/api/deliveries/:uid` | deliveries.edit | Update delivery status |

---

## Payment Integration

### M-Pesa STK Push Flow

```
1. Customer selects M-Pesa at checkout
2. Frontend normalises phone: 07xx → 2547xx
3. POST /api/payments/mpesa/stk-push
4. Backend calls Safaricom Daraja API
5. Customer receives STK push on phone
6. Customer enters M-Pesa PIN
7. Safaricom POSTs result to /api/payments/mpesa/callback
8. Frontend polls /api/payments/mpesa/status/:checkout_id every 3s
9. On success: payment.status = "success", mpesa_receipt saved
10. Driver status auto-set to "available" when order delivered
```

**Getting Sandbox credentials:**
1. Register at https://developer.safaricom.co.ke
2. Create an app → enable Lipa Na M-Pesa Sandbox
3. Copy Consumer Key + Consumer Secret
4. Sandbox shortcode: `174379`
5. Sandbox passkey: `bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919`
6. Test phone number: `254708374149`

**Going live:**
- Change `MPESA_ENV=production`
- Replace shortcode with your Paybill/Till number
- Replace passkey with your production passkey from Safaricom

---

### Flutterwave Card Payment Flow

```
1. Customer selects Card at checkout
2. POST /api/payments/card/initiate
3. Backend creates Flutterwave payment link
4. Frontend redirects to Flutterwave hosted page
5. Customer enters card details on Flutterwave's secure page
6. Two simultaneous events:
   a. Flutterwave POSTs to /api/payments/card/webhook
   b. Flutterwave redirects to /api/payments/card/verify
7. Backend verifies transaction with Flutterwave API
8. Customer lands on /customer?payment=success
```

**Test cards:**

| Card Type | Number | CVV | Expiry | PIN | OTP |
|---|---|---|---|---|---|
| Visa (success) | 4187427415564246 | 828 | 09/32 | 3310 | 12345 |
| Mastercard (success) | 5531886652142950 | 564 | 09/32 | 3310 | 12345 |
| Declined | 4242424242424242 | any | any | — | — |

**Going live:**
- Change `FLW_ENV=production`
- Replace test keys with live keys from Flutterwave dashboard

---

## Deployment (Render)

This backend is deployed on **Render** as a Web Service.

### Render configuration

| Setting | Value |
|---|---|
| Runtime | Python 3.12 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/` |

### Steps

1. Push your code to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Set the build and start commands above
5. Add all environment variables from the `.env` reference above
6. Add your PostgreSQL connection string under `DATABASE_URL`
7. Deploy

### Running migrations on Render

Add a one-off job or run via Render shell after first deploy:

```bash
alembic upgrade head
```

### Important notes for production

- Set `CORS` in `app/main.py` to allow only your Vercel frontend URL instead of `"*"`
- Set `APP_ENV=production` and `DEBUG=false`
- Use a strong random `JWT_SECRET_KEY` (minimum 32 characters)
- Set `MPESA_ENV=production` and `FLW_ENV=production` when going live
- The M-Pesa callback URL and Flutterwave redirect URL must be your Render URL

```python
# app/main.py — tighten CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```