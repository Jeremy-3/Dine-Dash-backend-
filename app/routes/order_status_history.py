from app.crud.order_status_history import crud_order_status_history
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID
from app.schemas.order_status_history import OrderStatusHistoryCreate, OrderStatusHistoryUpdate

router = APIRouter(prefix="/order-status-history", tags=["order-status-history"])

