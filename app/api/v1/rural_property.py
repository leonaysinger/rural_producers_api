from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import joinedload

from app.core.dependencies import DBSession
from app.core.security import get_current_user
from app.domain.models.property_crop import PropertyCrop
from app.domain.models.rural_property import RuralProperty
from app.domain.schemas.rural_property import RuralPropertyRead, RuralPropertyCreate, RuralPropertyUpdate
from app.repositories.rural_property import RuralPropertyRepository
from app.services.rural_property_service import RuralPropertyService

router = APIRouter(prefix="/properties", tags=["Rural Properties"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=RuralPropertyRead, status_code=status.HTTP_201_CREATED)
def create_rural_property(
    property_in: RuralPropertyCreate, db: DBSession
) -> RuralPropertyRead:
    repo = RuralPropertyService()
    return repo.create(db, property_in)

@router.get("/", response_model=list[RuralPropertyRead])
def list_rural_properties(
    db: DBSession,
    with_relations: bool = False
) -> list[RuralPropertyRead]:
    repo = RuralPropertyRepository()

    joins = []
    if with_relations:
        joins = [
            joinedload(RuralProperty.producer),
            joinedload(RuralProperty.crops).joinedload(PropertyCrop.crop),
            joinedload(RuralProperty.crops).joinedload(PropertyCrop.season),
        ]

    return repo.get_all(db, joins=joins)


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
    repo = RuralPropertyService()
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
