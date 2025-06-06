from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.models.crop import Crop
from app.domain.schemas.crop import CropCreate, CropUpdate
from app.repositories.base import BaseRepository


class CropRepository(BaseRepository):
    def __init__(self):
        super().__init__(Crop)

    def create(self, db: Session, crop_in: CropCreate) -> Crop:
        crop = Crop(**crop_in.dict())
        db.add(crop)
        db.commit()
        db.refresh(crop)
        return crop

    def update(self, db: Session, crop_id: UUID, crop_in: CropUpdate) -> Crop | None:
        crop = self.get_by_id(db, crop_id)
        if not crop:
            return None
        for field, value in crop_in.dict(exclude_unset=True).items():
            setattr(crop, field, value)
        db.commit()
        db.refresh(crop)
        return crop

    def delete(self, db: Session, crop_id: UUID) -> bool:
        crop = self.get_by_id(db, crop_id)
        if not crop:
            return False
        db.delete(crop)
        db.commit()
        return True

