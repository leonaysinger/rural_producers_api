from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.domain.schemas.property_crop import PropertyCropBaseRead, PropertyCropCreate
from app.domain.schemas.rural_producer import RuralProducerRead
from app.utils.validators import validate_property_areas


class RuralPropertyBase(BaseModel):
    name: str
    city: str
    state: str = Field(..., max_length=2, min_length=2)
    cep: str | None = None
    number: str | None = None
    description: str | None = None
    total_area: Decimal
    farming_area: Decimal
    vegetation_area: Decimal

    class Config:
        from_attributes = True


class RuralPropertyCreate(RuralPropertyBase):
    producer_id: UUID
    name: str | None = None
    city: str | None = None
    state: str | None = Field(None, max_length=2, min_length=2)
    cep: str | None = None
    number: str | None = None
    description: str | None = None
    total_area: Decimal | None = None
    farming_area: Decimal | None = None
    vegetation_area: Decimal | None = None
    crops: Optional[list[PropertyCropCreate]] = []

    @model_validator(mode="after")
    def validate_areas(self):
        if (
            self.total_area is not None and
            self.farming_area is not None and
            self.vegetation_area is not None
        ):
            validate_property_areas(
                self.total_area,
                self.farming_area,
                self.vegetation_area
            )
        return self


class RuralPropertyUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    state: str | None = Field(None, max_length=2, min_length=2)
    cep: str | None = None
    number: str | None = None
    description: str | None = None
    total_area: Decimal | None = None
    farming_area: Decimal | None = None
    vegetation_area: Decimal | None = None
    crops: Optional[list[PropertyCropCreate]] = []

    @model_validator(mode="after")
    def validate_areas(self):
        if (
            self.total_area is not None and
            self.farming_area is not None and
            self.vegetation_area is not None
        ):
            validate_property_areas(
                self.total_area,
                self.farming_area,
                self.vegetation_area
            )
        return self


class RuralPropertyRead(RuralPropertyBase):
    id: UUID
    producer_id: UUID
    created_at: datetime

    producer: Optional[RuralProducerRead] = None
    crops: list[PropertyCropBaseRead] = []

    class Config:
        from_attributes = True
