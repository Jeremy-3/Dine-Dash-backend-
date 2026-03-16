from sqlalchemy import Column, String, Integer, TIMESTAMP, Numeric, Boolean, ForeignKey, Text, text
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone


class Combo(Base):
    __tablename__ = "combos"

    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid         = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True, server_default=text("gen_random_uuid()"))
    name        = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    combo_price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at  = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at  = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    combo_items = relationship("ComboItem", back_populates="combo", cascade="all, delete-orphan")


class ComboItem(Base):
    __tablename__ = "combo_items"

    id       = Column(Integer, primary_key=True, index=True, autoincrement=True)
    combo_id = Column(Integer, ForeignKey("combos.id", ondelete="CASCADE"), nullable=False)
    food_id  = Column(Integer, ForeignKey("foods.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    # Relationships
    combo = relationship("Combo", back_populates="combo_items")
    food  = relationship("Food", back_populates="combo_items")