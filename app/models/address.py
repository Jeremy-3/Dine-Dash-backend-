from sqlalchemy import Column,String,Integer,TIMESTAMP,Text,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    street = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    

    # Relationships
    order = relationship("Order", back_populates="address")