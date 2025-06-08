from unittest.mock import MagicMock
from app.services.report import (
    get_summary,
    get_farms_by_state,
    get_farms_by_crop,
    get_land_usage
)

def test_get_summary():
    mock_session = MagicMock()
    mock_session.query.return_value.scalar.side_effect = [5, 200.5]

    result = get_summary(mock_session)

    assert result == {"total_farms": 5, "total_area": 200.5}
    assert mock_session.query.call_count == 2


def test_get_farms_by_state():
    mock_session = MagicMock()
    mock_session.query.return_value.group_by.return_value.all.return_value = [
        ("mg", 3),
        ("sp", 2),
    ]

    result = get_farms_by_state(mock_session)

    assert result == [
        {"name": "MG", "value": 3},
        {"name": "SP", "value": 2},
    ]
    mock_session.query.return_value.group_by.return_value.all.assert_called_once()


def test_get_farms_by_crop():
    mock_session = MagicMock()
    mock_session.query.return_value.join.return_value.group_by.return_value.all.return_value = [
        ("Soja", 4),
        ("Milho", 1),
    ]

    result = get_farms_by_crop(mock_session)

    assert result == [
        {"name": "Soja", "value": 4},
        {"name": "Milho", "value": 1},
    ]
    mock_session.query.return_value.join.return_value.group_by.return_value.all.assert_called_once()


def test_get_land_usage():
    mock_session = MagicMock()
    mock_session.query.return_value.one.return_value = (150.5, 49.5)

    result = get_land_usage(mock_session)

    assert result == [
        {"name": "Área Cultivável", "value": 150.5},
        {"name": "Área de Vegetação", "value": 49.5},
    ]
    mock_session.query.return_value.one.assert_called_once()
