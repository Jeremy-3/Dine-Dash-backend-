from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, Numeric, text
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone


class Order(Base):
    __tablename__ = "orders"

    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid           = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True, server_default=text("gen_random_uuid()"))
    customer_id   = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    driver_id     = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="SET NULL"), nullable=True)
    status        = Column(String, nullable=False, default="pending", index=True)
    subtotal      = Column(Numeric(10, 2), nullable=False)
    delivery_fee  = Column(Numeric(10, 2), nullable=False)
    total         = Column(Numeric(10, 2), nullable=False)
    created_at    = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at    = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships 
    customer = relationship(
        "User",
        foreign_keys="[Order.customer_id]",    # ← string form referencing column name
        back_populates="orders"
    )
    driver = relationship(
        "User",
        foreign_keys="[Order.driver_id]",      # ← string form referencing column name
    )
    restaurant = relationship(
        "Restaurant",
        foreign_keys="[Order.restaurant_id]",
        back_populates="orders"
    )

    order_items    = relationship("OrderItem",          back_populates="order", cascade="all, delete-orphan")
    address        = relationship("Address",            back_populates="order", uselist=False, cascade="all, delete-orphan")
    payment        = relationship("Payment",            back_populates="order", uselist=False, cascade="all, delete-orphan")
    delivery       = relationship("Delivery",           back_populates="order", uselist=False, cascade="all, delete-orphan")
    status_history = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")