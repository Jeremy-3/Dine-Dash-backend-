"""
FastAPI Database Seeder Script
Run with:
    python -m app.commands.seed_all
"""

from sqlalchemy.exc import IntegrityError
from app.core.config import settings 
from app.db.utils import db_context
from app.db.base import Base
from app.db.local_connector import engine
from app.core.security import hash_password
from app.core.constants import (
    DEFAULT_ROLES,
    DEFAULT_PERMISSIONS,
    DEFAULT_ROLE_PERMISSIONS,
    DEFAULT_USERS,
    DEFAULT_DRIVERS,
    DEFAULT_RESTAURANTS,
    DEFAULT_FOODS,
    DEFAULT_ORDERS,
    DEFAULT_ORDER_ITEMS,
    DEFAULT_ADDRESSES,
    DEFAULT_PAYMENTS,
    DEFAULT_DELIVERIES,
    DEFAULT_ORDER_STATUS_HISTORY,
    ROLE_SUPERADMIN_ID,
    DEFAULT_COMBOS,
)

from app.models.roles import Roles
from app.models.permissions import Permissions
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.driver import Driver
from app.models.restaurants import Restaurant
from app.models.foods import Food
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.address import Address
from app.models.payment import Payment
from app.models.deliveries import Delivery
from app.models.order_status_history import OrderStatusHistory
from app.models.combo import Combo 


def seed_table(db, model, data, table_name: str, flush: bool = False):
    print(f"Seeding {table_name}...")
    created = 0

    for row in data:
        pk = row.get("id")
        if pk is not None and db.get(model, pk):
            continue

        # Skip users if email is missing (Render-safe)
        if model == User and not row.get("email"):
            print(f"⚠️ Skipping user creation for missing email: {row}")
            continue

        obj = model(**row)
        db.add(obj)
        created += 1

    if flush:
        db.flush()
    db.commit()
    print(f"✓ Inserted {created} {table_name}")


def seed_role_permissions(db):
    print("Seeding role-permission mappings...")
    count = 0

    for role_id, permission_ids in DEFAULT_ROLE_PERMISSIONS.items():
        for permission_id in permission_ids:
            exists = (
                db.query(RolePermission)
                .filter_by(role_id=role_id, permission_id=permission_id)
                .first()
            )
            if not exists:
                db.add(RolePermission(role_id=role_id, permission_id=permission_id))
                count += 1

    db.commit()
    print(f"✓ Created {count} role-permission mappings")


def seed_superadmin(db):
    """Create a SUPERADMIN if env vars exist and not already in DB."""
    if not settings.SUPERADMIN_EMAIL:
        print("⚠️ SUPERADMIN_EMAIL not set, skipping admin creation")
        return

    exists = db.query(User).filter_by(email=settings.SUPERADMIN_EMAIL).first()
    if exists:
        print("✅ SUPERADMIN already exists, skipping")
        return

    user = User(
        name=settings.SUPERADMIN_NAME,
        email=settings.SUPERADMIN_EMAIL,
        phone=settings.SUPERADMIN_PHONE,
        password_hash=hash_password(settings.SUPERADMIN_PASSWORD),
        role_id=ROLE_SUPERADMIN_ID
    )
    db.add(user)
    db.commit()
    print("✓ SUPERADMIN created")


def seed_all():
    print("\n" + "=" * 60)
    print("Starting FastAPI database seeding")
    print("=" * 60 + "\n")

    if not settings.DATABASE_URL:
        print("❌ DATABASE_URL not set, skipping all seeding")
        return

    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")

    with db_context() as db:
        try:
            # === RBAC ===
            seed_table(db, Roles, DEFAULT_ROLES, "roles")
            seed_table(db, Permissions, DEFAULT_PERMISSIONS, "permissions")
            seed_role_permissions(db)

            # === SUPERADMIN ===
            seed_superadmin(db)

            # === USERS & DRIVERS ===
            seed_table(db, User, DEFAULT_USERS, "users", flush=True)
            seed_table(db, Driver, DEFAULT_DRIVERS, "drivers")

            # === RESTAURANTS & FOODS ===
            seed_table(db, Restaurant, DEFAULT_RESTAURANTS, "restaurants", flush=True)
            seed_table(db, Food, DEFAULT_FOODS, "foods")
            seed_table(db, Combo, DEFAULT_COMBOS, "combos")

            # === ORDERS ===
            seed_table(db, Order, DEFAULT_ORDERS, "orders", flush=True)
            seed_table(db, OrderItem, DEFAULT_ORDER_ITEMS, "order items")

            # === POST-ORDER ===
            seed_table(db, Address, DEFAULT_ADDRESSES, "addresses")
            seed_table(db, Payment, DEFAULT_PAYMENTS, "payments")
            seed_table(db, Delivery, DEFAULT_DELIVERIES, "deliveries")
            seed_table(db, OrderStatusHistory, DEFAULT_ORDER_STATUS_HISTORY, "order status history")

            print("\n" + "=" * 60)
            print("✓ Database seeding completed successfully")
            print("=" * 60)

        except IntegrityError as e:
            db.rollback()
            print("✗ Integrity error during seeding")
            raise e

        except Exception as e:
            db.rollback()
            print("✗ Seeding failed:", str(e))
            raise


if __name__ == "__main__":
    seed_all()