from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.models.rural_producer import RuralProducer
from app.domain.schemas.rural_producer import RuralProducerCreate, RuralProducerUpdate
from app.repositories.base import BaseRepository


class RuralProducerRepository(BaseRepository):
    def __init__(self):
        super().__init__(RuralProducer)

    def create(self, db: Session, producer_in: RuralProducerCreate) -> RuralProducer:
        producer = RuralProducer(**producer_in.dict())
        db.add(producer)
        db.commit()
        db.refresh(producer)
        return producer
    
    def update(self, db: Session, rural_producer_id: UUID, rural_producer_in: RuralProducerUpdate) -> RuralProducer | None:
        rural_producer = self.get_by_id(db, rural_producer_id)
        if not rural_producer:
            return None
        for field, value in rural_producer_in.dict(exclude_unset=True).items():
            setattr(rural_producer, field, value)
        db.commit()
        db.refresh(rural_producer)
        return rural_producer

    def delete(self, db: Session, rural_producer_id: UUID) -> bool:
        rural_producer = self.get_by_id(db, rural_producer_id)
        if not rural_producer:
            return False
        db.delete(rural_producer)
        db.commit()
        return True