from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.domain.models.rural_property import RuralProperty
from app.domain.schemas.rural_property import RuralPropertyCreate
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

            property_data = data.model_dump(exclude={"property_crops"})
            rural_property = self.property_repo.create(db, property_data)

            if data.property_crops:
                for property_crop in data.property_crops:
                    print(f"FFFFFFFFFFFFFFFF: ", property_crop)
                    property_crop.property_id = rural_property.id
                    self.property_crop_repo.create(db, property_crop)

            return rural_property

        except Exception as e:
            db.rollback()
            raise


