from sqlalchemy import Column,String,Integer,TIMESTAMP,Numeric,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base



class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id", ondelete="RESTRICT"), nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_order = Column(Numeric(10, 2), nullable=False)
    


    # Relationships
    order = relationship("Order", back_populates="order_items")
    food = relationship("Food", back_populates="order_items")