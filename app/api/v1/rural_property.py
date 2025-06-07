from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import DBSession
from app.domain.schemas.rural_property import RuralPropertyRead, RuralPropertyCreate, RuralPropertyUpdate
from app.repositories.rural_property import RuralPropertyRepository
from app.services.rural_property_service import RuralPropertyService

router = APIRouter(prefix="/properties", tags=["Rural Properties"])


@router.post("/", response_model=RuralPropertyRead, status_code=status.HTTP_201_CREATED)
def create_rural_property(
    property_in: RuralPropertyCreate, db: DBSession
) -> RuralPropertyRead:
    repo = RuralPropertyService()
    return repo.create(db, property_in)


@router.get("/", response_model=list[RuralPropertyRead])
def list_rural_properties(db: DBSession) -> list[RuralPropertyRead]:
    repo = RuralPropertyRepository()
    return repo.get_all(db)


@router.get("/{property_id}", response_model=RuralPropertyRead)
def get_rural_property(property_id: UUID, db: DBSession) -> RuralPropertyRead:
    repo = RuralPropertyRepository()
    rural_property = repo.get_by_id(db, property_id)
    if not rural_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return rural_property


@router.put("/{property_id}", response_model=RuralPropertyRead)
def update_rural_property(
    property_id: UUID, property_in: RuralPropertyUpdate, db: DBSession
) -> RuralPropertyRead:
    repo = RuralPropertyRepository()
    updated = repo.update(db, property_id, property_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Property not found")
    return updated


@router.delete("/{property_id}", response_model=bool)
def delete_rural_property(property_id: UUID, db: DBSession) -> bool:
    repo = RuralPropertyRepository()
    deleted = repo.delete(db, property_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")
    return True
