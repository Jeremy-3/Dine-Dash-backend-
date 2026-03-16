from app.crud.combo import crud_combo
from app.schemas.combo import ComboCreate, ComboUpdate, ComboOut
from app.dependencies.rbac import require_permission
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.response import ResponseModel
from uuid import UUID

router = APIRouter(prefix="/combos", tags=["combos"])


@router.get(
    "/available",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("combos.view"))]
)
def get_available_combos(db: Session = Depends(get_db)):
    combos = crud_combo.get_available_combos(db)
    return ResponseModel(
        data=[ComboOut.from_orm_with_items(c) for c in combos],
        message="Available combos retrieved successfully"
    )


@router.get(
    "/",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("combos.view"))]
)
def get_all_combos(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    combos, total = crud_combo.get_all_combos(db, page, limit)
    return ResponseModel(
        data=[ComboOut.from_orm_with_items(c) for c in combos],
        total=total,
        message="Combos retrieved successfully"
    )


@router.post(
    "/",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("combos.create"))]
)
def create_combo(combo_create: ComboCreate, db: Session = Depends(get_db)):
    combo = crud_combo.create_combo(db, combo_create)
    return ResponseModel(
        data=ComboOut.from_orm_with_items(combo),
        message="Combo created successfully"
    )


@router.get(
    "/{uid}",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("combos.view"))]
)
def get_combo(uid: UUID, db: Session = Depends(get_db)):
    combo = crud_combo.get_combo_by_uid(db, uid)
    return ResponseModel(
        data=ComboOut.from_orm_with_items(combo),
        message="Combo retrieved successfully"
    )


@router.put(
    "/{uid}",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("combos.edit"))]
)
def update_combo(uid: UUID, combo_update: ComboUpdate, db: Session = Depends(get_db)):
    combo = crud_combo.update_combo(db, uid, combo_update)
    return ResponseModel(
        data=ComboOut.from_orm_with_items(combo),
        message="Combo updated successfully"
    )


@router.delete(
    "/{uid}",
    response_model=ResponseModel,
    dependencies=[Depends(require_permission("combos.delete"))]
)
def delete_combo(uid: UUID, db: Session = Depends(get_db)):
    crud_combo.delete_combo(db, uid)
    return ResponseModel(message="Combo deleted successfully")