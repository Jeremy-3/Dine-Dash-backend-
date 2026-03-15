from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator
from app.schemas.constants import ORDER_STATUSES
from uuid import UUID
from typing import Optional, Union, List

class OrderItemInOrder(BaseModel):
    id: int
    food_id: int
    name: Optional[str] = None
    quantity: int
    price_at_order: Optional[Decimal] = None

    model_config = {"from_attributes": True}
 
class AddressInOrder(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}

class OrderAssign(BaseModel):
    driver_id: int
    restaurant_id: int

class OrderBase(BaseModel):
    customer_id: int
    status: str
    subtotal: Decimal
    delivery_fee: Decimal
    total: Decimal

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str):
        if v not in ORDER_STATUSES:
            raise ValueError(f"Invalid order status: {v}")
        return v

    @field_validator("subtotal", "delivery_fee", "total")
    @classmethod
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("Amount must be >= 0")
        return v


class OrderCreate(BaseModel):
    customer_id: int
    delivery_fee: Decimal = Decimal("4.99")

    @field_validator("delivery_fee")
    @classmethod
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("Amount must be >= 0")
        return v


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    subtotal: Optional[Decimal] = None
    delivery_fee: Optional[Decimal] = None
    total: Optional[Decimal] = None
    driver_id: Optional[int] = None         
    restaurant_id: Optional[int] = None 

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str):
        if v is not None and v not in ORDER_STATUSES:
            raise ValueError(f"Invalid order status: {v}")
        return v

    @field_validator("subtotal", "delivery_fee", "total")
    @classmethod
    def non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Amount must be >= 0")
        return v


class OrderOut(BaseModel):
    id: int
    uid: Union[str, UUID]
    customer_id: int
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None      
    driver_id: Optional[int] = None
    driver_name: Optional[str] = None
    restaurant_id: Optional[int] = None
    restaurant_name: Optional[str] = None
    status: str
    subtotal: Decimal
    delivery_fee: Decimal
    total: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemInOrder] = []
    delivery_address: Optional[AddressInOrder] = None   

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_with_items(cls, order) -> "OrderOut":
        items = []
        for oi in (order.order_items or []):
            items.append(OrderItemInOrder(
                id=oi.id,
                food_id=oi.food_id,
                name=oi.food.name if oi.food else None,
                quantity=oi.quantity,
                price_at_order=oi.price_at_order,
            ))

        # Extract delivery address from order.address relationship
        delivery_address = None
        if order.address:
            delivery_address = AddressInOrder(
                street=order.address.street,
                city=order.address.city,
                state=order.address.state,
                zip_code=order.address.zip_code,
                notes=order.address.notes,
            )

        return cls(
            id=order.id,
            uid=order.uid,
            customer_id=order.customer_id,
            customer_name=order.customer.name if order.customer else None,
            customer_phone=order.customer.phone if order.customer else None,  
            driver_id=order.driver_id,
            driver_name=order.driver.name if order.driver else None,
            restaurant_id=order.restaurant_id,
            restaurant_name=order.restaurant.name if order.restaurant else None,
            status=order.status,
            subtotal=order.subtotal,
            delivery_fee=order.delivery_fee,
            total=order.total,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=items,
            delivery_address=delivery_address,   
        )