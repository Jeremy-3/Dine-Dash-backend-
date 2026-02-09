from datetime import datetime, timezone
from sqlalchemy import Column,String,Integer,TIMESTAMP,Numeric,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    amount = Column(Numeric(10, 2), nullable=False)
    method = Column(String, default="debit_card", nullable=False)
    status = Column(String, default="pending",nullable=False)
    paid_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)) # timezone = True ensures that the column is timezone-aware. # lambda function, ensures that a new timestamp is generated each time a record is created or updated.

    
    # Relationships
    order = relationship("Order", back_populates="payment")