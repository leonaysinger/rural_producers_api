from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.core.dependencies import DBSession
from app.domain.schemas.rural_producer import RuralProducerRead, RuralProducerCreate, RuralProducerUpdate

from app.repositories.rural_producer import RuralProducerRepository

router = APIRouter(prefix="/producers", tags=["Rural Producers"])


@router.post("/", response_model=RuralProducerRead)
def create_producer(producer_in: RuralProducerCreate,
                    db: DBSession) -> RuralProducerRead:
    repo = RuralProducerRepository()
    return repo.create(db, producer_in)


@router.get("/", response_model=list[RuralProducerRead])
def list_producers(db: DBSession) -> list[RuralProducerRead]:
    repo = RuralProducerRepository()
    return repo.get_all(db)


@router.get("/{producer_id}", response_model=RuralProducerRead)
def get_producer(producer_id: UUID, db: DBSession) -> RuralProducerRead:
    repo = RuralProducerRepository()
    producer = repo.get_by_id(db, producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer


@router.put("/{producer_id}", response_model=RuralProducerRead)
def update_producer(
    producer_id: UUID, producer_in: RuralProducerUpdate, db: DBSession
) -> RuralProducerRead:
    repo = RuralProducerRepository()
    producer = repo.update(db, producer_id, producer_in)
    if not producer:
        raise HTTPException(status_code=404, detail="Producer not found")
    return producer


@router.delete("/{producer_id}", response_model=bool)
def delete_producer(producer_id: UUID, db: DBSession) -> bool:
    repo = RuralProducerRepository()
    return repo.delete(db, producer_id)
