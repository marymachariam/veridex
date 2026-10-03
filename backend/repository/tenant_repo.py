from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base

ModelT = TypeVar("ModelT", bound=Base)


class TenantRepository(Generic[ModelT]):
    """CRUD that can only ever see rows belonging to the given company_id."""

    def __init__(self, model: Type[ModelT]):
        self.model = model

    def get(self, db: Session, company_id: int, obj_id: int) -> Optional[ModelT]:
        stmt = select(self.model).where(self.model.id == obj_id, self.model.company_id == company_id)
        return db.scalar(stmt)

    def list_all(self, db: Session, company_id: int, *, skip: int = 0, limit: int = 100, **filters):
        stmt = select(self.model).where(self.model.company_id == company_id)
        for column, value in filters.items():
            if value is not None:
                stmt = stmt.where(getattr(self.model, column) == value)
        stmt = stmt.order_by(self.model.id.desc()).offset(skip).limit(limit)
        return list(db.scalars(stmt))

    def create(self, db: Session, company_id: int, data: dict) -> ModelT:
        obj = self.model(company_id=company_id, **data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: ModelT, data: dict) -> ModelT:
        for key, value in data.items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: ModelT) -> None:
        db.delete(obj)
        db.commit()