from datetime import datetime, timezone
from sqlalchemy import Column,String,Integer,TIMESTAMP,Numeric,ForeignKey,text
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(UUID(as_uuid=True), unique=True, nullable=False,
             index=True, server_default=text("gen_random_uuid()"))
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    amount = Column(Numeric(10, 2), nullable=False)
    method = Column(String, nullable=False)
    phone = Column(String(20), nullable=True)
    checkout_request_id = Column(String(255), unique=True, nullable=True)
    mpesa_receipt = Column(String(255), unique=True, nullable=True)
    tx_ref = Column(String(255), nullable=True, unique=True)
    flw_tx_id = Column(String(100), nullable=True)
    status = Column(String, default="pending",nullable=False)
    paid_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)) # timezone = True ensures that the column is timezone-aware. # lambda function, ensures that a new timestamp is generated each time a record is created or updated.

    
    # Relationships
    order = relationship("Order", back_populates="payment")