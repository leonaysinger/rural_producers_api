from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain.models.rural_producer import RuralProducer
from app.domain.models.rural_property import RuralProperty
from app.domain.schemas.rural_property import RuralPropertyCreate, RuralPropertyUpdate
from app.repositories.rural_property import RuralPropertyRepository


def test_create_rural_property(rural_property_mock):
    mock_session = MagicMock()
    repo = RuralPropertyRepository()

    property = repo.create(mock_session, rural_property_mock)

    assert property.name == "Test"
    assert property.city == "Florianópolis"
    assert property.cep == "00000000"
    mock_session.add.assert_called_once_with(property)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(property)

def test_update_rural_property_success(rural_property_mock):
    mock_session = MagicMock()
    repo = RuralPropertyRepository()

    rural_producer_id = uuid4()
    repo.get_by_id = MagicMock(return_value=rural_property_mock)

    update_data = RuralPropertyUpdate(name="P1")

    updated_rural_producer = repo.update(mock_session, rural_producer_id, update_data)

    assert updated_rural_producer.name == "P1"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(rural_property_mock)


def test_get_all_properties(rural_property_mock):
    mock_session = MagicMock()
    repo = RuralPropertyRepository()

    expected_producers = [ rural_property_mock ]
    mock_session.query.return_value.all.return_value = expected_producers

    result = repo.get_all(mock_session)

    assert result == expected_producers
    mock_session.query.assert_called_once_with(RuralProperty)
    mock_session.query.return_value.all.assert_called_once()

def test_delete_rural_property_success(rural_property_mock):
    mock_session = MagicMock()
    repo = RuralPropertyRepository()

    rural_producer_id = uuid4()
    repo.get_by_id = MagicMock(return_value=rural_property_mock)

    result = repo.delete(mock_session, rural_producer_id)

    assert result is True
    mock_session.delete.assert_called_once_with(rural_property_mock)
    mock_session.commit.assert_called_once()