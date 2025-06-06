# app/api/v1/season.py

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import DBSession
from app.domain.schemas.season import SeasonCreate, SeasonRead, SeasonUpdate
from app.repositories.season import SeasonRepository

router = APIRouter(prefix='/seasons')


@router.post("/", response_model=SeasonRead, status_code=status.HTTP_201_CREATED)
def create_season(season_in: SeasonCreate, db: DBSession) -> SeasonRead:
    repo = SeasonRepository()
    return repo.create(db, season_in)


@router.put("/{season_id}", response_model=SeasonRead)
def update_season(season_id: UUID, season_in: SeasonUpdate, db: DBSession) -> SeasonRead:
    repo = SeasonRepository()
    updated = repo.update(db, season_id, season_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Season not found")
    return updated


@router.get("/", response_model=list[SeasonRead])
def list_seasons(db: DBSession) -> list[SeasonRead]:
    repo = SeasonRepository()
    return repo.get_all(db)


@router.get("/{season_id}", response_model=SeasonRead)
def get_season(season_id: UUID, db: DBSession) -> SeasonRead:
    repo = SeasonRepository()
    season = repo.get_by_id(db, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season


@router.delete("/{season_id}", response_model=bool)
def delete_crop(season_id: UUID, db: DBSession) -> bool:
    repo = SeasonRepository()
    return repo.delete(db, season_id)
