from pydantic import BaseModel, field_validator
from typing import Optional, Union
from uuid import UUID
from datetime import datetime
from app.schemas.constants import DRIVER_STATUSES
from app.schemas.user import UserOut


class DriverBase(BaseModel):
    user_id: int
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in DRIVER_STATUSES:
            raise ValueError(f"Invalid driver status: {v}")
        return v


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in DRIVER_STATUSES:
            raise ValueError(f"Invalid driver status: {v}")
        return v


class DriverOut(BaseModel):          # ← don't inherit DriverBase, define cleanly
    id: int
    uid: Union[str, UUID]
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[UserOut] = None   # ← nested user with name/email/phone

    model_config = {"from_attributes": True}