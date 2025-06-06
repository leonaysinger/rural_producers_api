from unittest.mock import MagicMock
from uuid import uuid4
from app.repositories.crop import CropRepository
from app.domain.models.crop import Crop
from app.domain.schemas.crop import CropCreate, CropUpdate


def test_create_crop():
    mock_session = MagicMock()
    repo = CropRepository()

    crop_data = CropCreate(name="Milho")
    crop = repo.create(mock_session, crop_data)

    assert crop.name == "Milho"
    mock_session.add.assert_called_once_with(crop)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(crop)


def test_update_crop_success():
    mock_session = MagicMock()
    repo = CropRepository()

    crop_id = uuid4()
    existing_crop = Crop(id=crop_id, name="Soybean",)
    repo.get_by_id = MagicMock(return_value=existing_crop)

    update_data = CropUpdate(name="Rice")

    updated_crop = repo.update(mock_session, crop_id, update_data)

    assert updated_crop.name == "Rice"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(existing_crop)


def test_update_crop_not_found():
    mock_session = MagicMock()
    repo = CropRepository()

    crop_id = uuid4()
    repo.get_by_id = MagicMock(return_value=None)

    update_data = CropUpdate(name="Bean")
    result = repo.update(mock_session, crop_id, update_data)

    assert result is None
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


def test_delete_crop_success():
    mock_session = MagicMock()
    repo = CropRepository()

    crop_id = uuid4()
    crop = Crop(id=crop_id, name="wheat")
    repo.get_by_id = MagicMock(return_value=crop)

    result = repo.delete(mock_session, crop_id)

    assert result is True
    mock_session.delete.assert_called_once_with(crop)
    mock_session.commit.assert_called_once()


def test_delete_crop_not_found():
    mock_session = MagicMock()
    repo = CropRepository()

    crop_id = uuid4()
    repo.get_by_id = MagicMock(return_value=None)

    result = repo.delete(mock_session, crop_id)

    assert result is False
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()
