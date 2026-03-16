from pydantic import BaseModel, field_validator
from typing import Optional, Union, List
from decimal import Decimal
from uuid import UUID
from datetime import datetime


class ComboItemBase(BaseModel):
    food_id: int
    quantity: int = 1


class ComboItemOut(BaseModel):
    id: int
    food_id: int
    quantity: int
    food_name: Optional[str] = None
    food_price: Optional[Decimal] = None

    model_config = {"from_attributes": True}


class ComboBase(BaseModel):
    name: str
    description: Optional[str] = None
    combo_price: Decimal
    is_available: bool = True

    @field_validator("combo_price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Combo price must be greater than 0")
        return v


class ComboCreate(ComboBase):
    items: List[ComboItemBase] = []   # food items included in this combo


class ComboUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    combo_price: Optional[Decimal] = None
    is_available: Optional[bool] = None
    items: Optional[List[ComboItemBase]] = None

    @field_validator("combo_price")
    @classmethod
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Combo price must be greater than 0")
        return v


class ComboOut(ComboBase):
    id: int
    uid: Union[str, UUID]
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[ComboItemOut] = []
    original_total: Optional[Decimal] = None   # sum of individual food prices
    savings: Optional[Decimal] = None          # original_total - combo_price

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_with_items(cls, combo) -> "ComboOut":
        items = []
        original_total = Decimal("0")

        for ci in (combo.combo_items or []):
            food_price = ci.food.price if ci.food else Decimal("0")
            original_total += food_price * ci.quantity
            items.append(ComboItemOut(
                id=ci.id,
                food_id=ci.food_id,
                quantity=ci.quantity,
                food_name=ci.food.name if ci.food else None,
                food_price=food_price,
            ))

        savings = original_total - combo.combo_price

        return cls(
            id=combo.id,
            uid=combo.uid,
            name=combo.name,
            description=combo.description,
            combo_price=combo.combo_price,
            is_available=combo.is_available,
            created_at=combo.created_at,
            updated_at=combo.updated_at,
            items=items,
            original_total=original_total,
            savings=savings if savings > 0 else Decimal("0"),
        )