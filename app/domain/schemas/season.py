# app/domain/schemas/season.py
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class SeasonBase(BaseModel):
    name: str
    year: int


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None


class SeasonRead(SeasonBase):
    id: UUID
