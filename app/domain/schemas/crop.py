# app/domain/schemas/test_crop_repository.py

from uuid import UUID

from pydantic import BaseModel


class CropBase(BaseModel):
    name: str


class CropCreate(CropBase):
    pass


class CropUpdate(CropBase):
    pass


class CropRead(CropBase):
    id: UUID
