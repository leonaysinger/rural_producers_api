from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.models.season import Season
from app.domain.schemas.season import SeasonCreate, SeasonUpdate
from app.repositories.base import BaseRepository


class SeasonRepository(BaseRepository):
    def __init__(self):
        super().__init__(Season)

    def create(self, db: Session, season_in: SeasonCreate) -> Season:
        season = Season(**season_in.dict())
        db.add(season)
        db.commit()
        db.refresh(season)
        return season

    def update(self, db: Session, season_id: UUID, season_in: SeasonUpdate) -> Season | None:
        season = self.get_by_id(db, season_id)
        if not season:
            return None

        for field, value in season_in.dict(exclude_unset=True).items():
            setattr(season, field, value)

        db.commit()
        db.refresh(season)
        return season

    def delete(self, db: Session, season_id: UUID) -> bool:
        season = self.get_by_id(db, season_id)
        if not season:
            return False
        db.delete(season)
        db.commit()
        return True
