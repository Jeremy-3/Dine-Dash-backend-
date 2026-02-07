from sqlalchemy import Column ,String ,Integer,TIMESTAMP,func,Text
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID 
import uuid

class Permissions(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True)
    uid=Column(UUID(as_uuid=True),unique=True,default=uuid.uuid4,nullable=False,index=True)
    name = Column(String, unique=True)
    description=Column(Text)
    category=Column(String(50))
    
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), nullable=False) # lambda function, ensures that a new timestamp is generated each time a record is created or updated.
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)



    role_permissions = relationship("RolePermission", back_populates="permission")
    