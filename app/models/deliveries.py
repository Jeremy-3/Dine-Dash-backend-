from sqlalchemy import Column,String,Integer,TIMESTAMP,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Delivery(Base):
    __tablename__ = "deliveries"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="RESTRICT"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="RESTRICT"), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status = Column(String, nullable=False, default="assigned", index=True)
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    delivered_at = Column(DateTime, nullable=True)
    

    # Relationships
    order = relationship("Order", back_populates="delivery")
    driver = relationship("Driver", foreign_keys=[driver_id], back_populates="deliveries")
    restaurant = relationship("Restaurant", back_populates="deliveries")
    manager = relationship("User", foreign_keys=[assigned_by], back_populates="assigned_deliveries")