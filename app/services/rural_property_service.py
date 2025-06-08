from uuid import UUID

from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.domain.models.rural_property import RuralProperty
from app.domain.schemas.rural_property import RuralPropertyCreate, RuralPropertyUpdate
from app.repositories.propety_crops import PropertyCropRepository
from app.repositories.rural_producer import RuralProducerRepository
from app.repositories.rural_property import RuralPropertyRepository


class RuralPropertyService:
    def __init__(self):
        self.producer_repo = RuralProducerRepository()
        self.property_repo = RuralPropertyRepository()
        self.property_crop_repo = PropertyCropRepository()

    def create(self, db: Session, data: RuralPropertyCreate) -> RuralProperty:
        try:
            producer = self.producer_repo.get_by_id(db, data.producer_id)
            if not producer:
                raise HTTPException(status_code=404, detail="Producer not found")

            property_data = data.model_dump(exclude={"crops"})
            rural_property = self.property_repo.create(db, property_data)

            if data.crops:
                for property_crop in data.crops:
                    property_crop.property_id = rural_property.id
                    self.property_crop_repo.create(db, property_crop)

            db.commit()
            return rural_property

        except Exception as e:
            db.rollback()
            raise

    def update(self, db: Session, property_id: UUID, data: RuralPropertyUpdate) -> RuralProperty:
        try:
            rural_property = self.property_repo.get_by_id(db, property_id)
            if not rural_property:
                raise HTTPException(status_code=404, detail="Property not found")

            update_data = data.model_dump(exclude_unset=True, exclude={"crops"})
            for key, value in update_data.items():
                setattr(rural_property, key, value)

            if data.crops is not None:
                self.property_crop_repo.delete_by_property_id(db, property_id)
                for crop in data.crops:
                    crop.property_id = property_id
                    self.property_crop_repo.create(db, crop)

            db.commit()
            db.refresh(rural_property)
            return rural_property

        except Exception as e:
            db.rollback()
            raise e