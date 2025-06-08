# app/infrastructure/repositories/base.py

from typing import TypeVar, Optional, Sequence

from sqlalchemy.orm import Session, joinedload, Load
from sqlalchemy.orm.decl_api import DeclarativeMeta

T = TypeVar("T")


class BaseRepository:
    def __init__(self, model: type[DeclarativeMeta]):
        self.model = model

    def get_all(self, db: Session, joins: list = None) -> list[T]:
        query = db.query(self.model)
        if joins:
            for join in joins:
                query = query.options(join)
        return query.all()

    def get_by_id(self, db: Session, id: str):
        return db.query(self.model).filter(self.model.id == id).first()

    def deactivate(self, db: Session, id: str) -> bool:
        if "is_active" not in self.model.__table__.columns.keys():
            raise AttributeError(
                f"Model '{self.model.__name__}' has no attribute 'is_active'"
            )

        instance = db.query(self.model).filter(self.model.id == id).first()
        if not instance:
            return False

        instance.is_active = False
        db.commit()
        db.refresh(instance)
        return True
