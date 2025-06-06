# app/api/v1/crop.py

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import DBSession
from app.domain.schemas.crop import CropRead, CropCreate, CropUpdate
from app.repositories.crop import CropRepository

router = APIRouter(prefix="/crops")


@router.post("/", response_model=CropRead, status_code=status.HTTP_201_CREATED)
def create_crop(crop_in: CropCreate, db: DBSession) -> CropRead:
    repo = CropRepository()
    return repo.create(db, crop_in)


@router.get("/", response_model=list[CropRead])
def list_crops(db: DBSession) -> list[CropRead]:
    repo = CropRepository()
    return repo.get_all(db)


@router.get("/{crop_id}", response_model=CropRead)
def get_crop(crop_id: UUID, db: DBSession) -> CropRead:
    repo = CropRepository()
    crop = repo.get_by_id(db, crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop


@router.put("/{crop_id}", response_model=CropRead)
def update_crop(crop_id: UUID, crop_in: CropUpdate, db: DBSession) -> CropRead:
    repo = CropRepository()
    crop = repo.update(db, crop_id, crop_in)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop


@router.delete("/{crop_id}", response_model=bool)
def delete_crop(crop_id: UUID, db: DBSession) -> bool:
    repo = CropRepository()
    return repo.delete(db, crop_id)
