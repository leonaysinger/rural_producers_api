from unittest.mock import MagicMock

from app.services.report import get_summary, get_farms_by_state, get_farms_by_crop, get_land_usage


def test_get_summary():
    mock_session = MagicMock()

    # mock do count e sum
    mock_session.query.return_value.scalar.side_effect = [5, 200.5]

    result = get_summary(mock_session)

    assert result == {"total_farms": 5, "total_area": 200.5}
    assert mock_session.query.call_count == 2


def test_get_farms_by_state():
    mock_session = MagicMock()

    # mock do all()
    mock_session.query.return_value.group_by.return_value.all.return_value = [
        ("MG", 3),
        ("SP", 2),
    ]

    result = get_farms_by_state(mock_session)

    assert result == {"MG": 3, "SP": 2}
    mock_session.query.return_value.group_by.return_value.all.assert_called_once()


def test_get_farms_by_crop():
    mock_session = MagicMock()

    # mock do all()
    mock_session.query.return_value.join.return_value.group_by.return_value.all.return_value = [
        ("Soja", 4),
        ("Milho", 1),
    ]

    result = get_farms_by_crop(mock_session)

    assert result == {"Soja": 4, "Milho": 1}
    mock_session.query.return_value.join.return_value.group_by.return_value.all.assert_called_once()


def test_get_land_usage():
    mock_session = MagicMock()

    # mock do one()
    mock_session.query.return_value.one.return_value = (150.5, 49.5)

    result = get_land_usage(mock_session)

    assert result == {"farming_area": 150.5, "vegetation_area": 49.5}
    mock_session.query.return_value.one.assert_called_once()
