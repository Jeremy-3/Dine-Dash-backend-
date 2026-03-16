from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from uuid import UUID
from app.models.combo import Combo, ComboItem
from app.schemas.combo import ComboCreate, ComboUpdate
from app.crud.base import CRUDBase

MODEL = Combo


class CRUDCombo(CRUDBase[MODEL, ComboCreate]):

    def _load_with_items(self, db: Session, combo_id: int) -> Combo:
        return (
            db.query(Combo)
            .options(joinedload(Combo.combo_items).joinedload(ComboItem.food))
            .filter(Combo.id == combo_id)
            .first()
        )

    def create_combo(self, db: Session, combo_in: ComboCreate) -> Combo:
        combo = Combo(
            name=combo_in.name,
            description=combo_in.description,
            combo_price=combo_in.combo_price,
            is_available=combo_in.is_available,
        )
        db.add(combo)
        db.flush()

        for item in combo_in.items:
            db.add(ComboItem(
                combo_id=combo.id,
                food_id=item.food_id,
                quantity=item.quantity,
            ))

        db.commit()
        return self._load_with_items(db, combo.id)

    def get_all_combos(self, db: Session, page: int = 1, limit: int = 50):
        query = (
            db.query(Combo)
            .options(joinedload(Combo.combo_items).joinedload(ComboItem.food))
            .order_by(Combo.created_at.desc())
        )
        total  = query.count()
        combos = query.offset((page - 1) * limit).limit(limit).all()
        return combos, total

    def get_available_combos(self, db: Session):
        return (
            db.query(Combo)
            .options(joinedload(Combo.combo_items).joinedload(ComboItem.food))
            .filter(Combo.is_available == True)
            .all()
        )

    def get_combo_by_uid(self, db: Session, uid: UUID) -> Combo:
        combo = (
            db.query(Combo)
            .options(joinedload(Combo.combo_items).joinedload(ComboItem.food))
            .filter(Combo.uid == uid)
            .first()
        )
        if not combo:
            raise HTTPException(status_code=404, detail="Combo not found")
        return combo

    def update_combo(self, db: Session, uid: UUID, combo_in: ComboUpdate) -> Combo:
        combo = self.get_record_by_field(db, "uid", uid)
        if not combo:
            raise HTTPException(status_code=404, detail="Combo not found")

        if combo_in.name        is not None: combo.name         = combo_in.name
        if combo_in.description is not None: combo.description  = combo_in.description
        if combo_in.combo_price is not None: combo.combo_price  = combo_in.combo_price
        if combo_in.is_available is not None: combo.is_available = combo_in.is_available

        # Replace items if provided
        if combo_in.items is not None:
            db.query(ComboItem).filter(ComboItem.combo_id == combo.id).delete()
            for item in combo_in.items:
                db.add(ComboItem(combo_id=combo.id, food_id=item.food_id, quantity=item.quantity))

        db.commit()
        return self._load_with_items(db, combo.id)

    def delete_combo(self, db: Session, uid: UUID):
        combo = self.get_record_by_field(db, "uid", uid)
        if not combo:
            raise HTTPException(status_code=404, detail="Combo not found")
        db.delete(combo)
        db.commit()


crud_combo = CRUDCombo(MODEL)