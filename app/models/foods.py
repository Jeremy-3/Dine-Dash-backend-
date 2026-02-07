from sqlalchemy import Column,String,Integer,TIMESTAMP,Numeric,Boolean,Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime,timezone



class Food(Base):
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100),index=True)
    price = Column(Numeric(10, 2), nullable=False)
    available = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),  nullable=False) # timezone = True ensures that the column is timezone-aware. # lambda function, ensures that a new timestamp is generated each time a record is created or updated.
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc),  nullable=False)


    
    # Relationships
    order_items = relationship("OrderItem", back_populates="food")