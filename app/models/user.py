from sqlalchemy import Column,String, Integer,TIMESTAMP,func,ForeignKey,text,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID 

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid = Column(UUID(as_uuid=True),unique=True,nullable=False,index=True,server_default=text("gen_random_uuid()"))      
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),  nullable=False) # timezone = True ensures that the column is timezone-aware. # lambda function, ensures that a new timestamp is generated each time a record is created or updated.
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc),  nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, server_default=text("TRUE"))

    # Relationships
    role = relationship("Roles", back_populates="users", foreign_keys=[role_id], lazy='joined')
    driver_profile = relationship("Driver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order",foreign_keys="Order.customer_id", back_populates="customer")
    assigned_deliveries = relationship("Delivery", foreign_keys="Delivery.assigned_by", back_populates="manager")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
    
    
