from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.models.property_crop import PropertyCrop
from app.domain.schemas.property_crop import PropertyCropCreate
from app.repositories.base import BaseRepository


class PropertyCropRepository(BaseRepository):
    def __init__(self):
        super().__init__(PropertyCrop)

    def create(self, db: Session, crop_in: PropertyCropCreate) -> PropertyCrop:
        crop = PropertyCrop(**crop_in.dict())
        db.add(crop)
        db.commit()
        db.refresh(crop)
        return crop


    def delete(self, db: Session, property_crop_id: UUID) -> bool:
        crop = self.get_by_id(db, property_crop_id)
        if not crop:
            return False
        db.delete(crop)
        db.commit()
        return True

    def delete_by_property_id(self, db: Session, property_id: UUID) -> int:
        count = db.query(self.model).filter(self.model.property_id == property_id).delete()
        db.commit()
        return count