from unittest.mock import MagicMock
from uuid import uuid4

from app.domain.models.season import Season
from app.domain.schemas.season import SeasonCreate, SeasonUpdate
from app.repositories.season import SeasonRepository


def test_create_season():
    mock_session = MagicMock()
    repo = SeasonRepository()

    season_data = SeasonCreate(name="Winter", year=2025)
    season = repo.create(mock_session, season_data)

    assert season.name == "Winter"
    mock_session.add.assert_called_once_with(season)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(season)


def test_update_crop_success():
    mock_session = MagicMock()
    repo = SeasonRepository()

    season_id = uuid4()
    existing_crop = Season(id=season_id, name="Spring",)
    repo.get_by_id = MagicMock(return_value=existing_crop)

    update_data = SeasonUpdate(name="Spring 2")

    updated_season = repo.update(mock_session, season_id, update_data)

    assert updated_season.name == "Spring 2"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(existing_crop)


def test_delete_crop_success():
    mock_session = MagicMock()
    repo = SeasonRepository()

    crop_id = uuid4()
    crop = Season(id=crop_id, name="winter")
    repo.get_by_id = MagicMock(return_value=crop)

    result = repo.delete(mock_session, crop_id)

    assert result is True
    mock_session.delete.assert_called_once_with(crop)
    mock_session.commit.assert_called_once()