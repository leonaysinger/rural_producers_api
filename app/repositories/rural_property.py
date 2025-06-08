from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.models.rural_property import RuralProperty
from app.domain.schemas.rural_property import RuralPropertyUpdate, RuralPropertyCreate
from app.repositories.base import BaseRepository


class RuralPropertyRepository(BaseRepository):
    def __init__(self):
        super().__init__(RuralProperty)

    def create(self, db: Session, property_in: RuralPropertyCreate) -> RuralProperty:
        if isinstance(property_in, dict):
            data = property_in
        else:
            data = property_in.model_dump(exclude={"crops"})

        rural_property = RuralProperty(**data)
        db.add(rural_property)
        db.flush()
        db.refresh(rural_property)
        return rural_property

    def update(self, db: Session, property_id: UUID, property_in: RuralPropertyUpdate) -> RuralProperty | None:
        rural_property = self.get_by_id(db, property_id)
        if not rural_property:
            return None

        for field, value in property_in.model_dump(exclude_unset=True).items():
            setattr(rural_property, field, value)

        db.commit()
        db.refresh(rural_property)
        return rural_property

    def delete(self, db: Session, property_id: UUID) -> bool:
        rural_property = self.get_by_id(db, property_id)
        if not rural_property:
            return False

        db.delete(rural_property)
        db.commit()
        return True