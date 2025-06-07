import uuid

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class RuralProperty(Base):
    __tablename__ = "rural_properties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producer_id = Column(UUID(as_uuid=True), ForeignKey("rural_producers.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String(2), nullable=False)
    cep = Column(String, nullable=True)
    number = Column(String, nullable=True)
    description = Column(String, nullable=True)
    total_area = Column(Numeric(10, 2), nullable=False)
    farming_area = Column(Numeric(10, 2), nullable=False)
    vegetation_area = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("farming_area + vegetation_area <= total_area", name="chk_area_limit"),
    )

    producer = relationship("RuralProducer", back_populates="properties")
    crops = relationship("PropertyCrop", back_populates="property", cascade="all, delete-orphan")


