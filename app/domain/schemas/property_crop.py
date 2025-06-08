from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PropertyCropBase(BaseModel):
    id: str


class PropertyCropCreate(BaseModel):
    season_id: UUID
    crop_id: UUID
    property_id: Optional[UUID] = None


class PropertyCropBaseUpdate(PropertyCropBase):
    pass


class PropertyCropBaseRead(PropertyCropBase):
    id: UUID
    season_id: UUID
    crop_id: UUID
