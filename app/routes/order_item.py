from app.crud.order_item import crud_order_item
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db   
from app.schemas.response import ResponseModel
from uuid import UUID   


router = APIRouter(prefix="/order-items", tags=["order-items"])

