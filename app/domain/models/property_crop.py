# app/domain/models/property_crop.py

import uuid
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class PropertyCrop(Base):
    __tablename__ = "property_crops"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    property_id = Column(UUID(as_uuid=True), ForeignKey("rural_properties.id", ondelete="CASCADE"), nullable=False)
    season_id = Column(UUID(as_uuid=True), ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False)
    crop_id = Column(UUID(as_uuid=True), ForeignKey("crops.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("property_id", "season_id", "crop_id", name="uix_property_crop"),
    )

    property = relationship("RuralProperty", back_populates="crops")
    season = relationship("Season")
    crop = relationship("Crop")
