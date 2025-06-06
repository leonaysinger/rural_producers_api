from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain.models.rural_producer import RuralProducer
from app.domain.schemas.rural_producer import RuralProducerCreate, RuralProducerUpdate
from app.repositories.rural_producer import RuralProducerRepository


def test_create_rural_producer_with_cpf(valid_cpf):
    mock_session = MagicMock()
    repo = RuralProducerRepository()

    producer_data = RuralProducerCreate(name="Test", document_type="CPF", document=valid_cpf)
    producer = repo.create(mock_session, producer_data)

    assert producer.name == "Test"
    assert producer.document_type == "CPF"
    assert producer.document == "48216327056"
    mock_session.add.assert_called_once_with(producer)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(producer)

def test_create_rural_producer_with_invalid_cpf_should_return_error(invalid_cpf):

    with pytest.raises(ValidationError) as exc_info:
        RuralProducerCreate(
            name="Test",
            document_type="CPF",
            document=invalid_cpf
        )

    assert "Invalid CPF" in str(exc_info.value)

def test_create_rural_producer_with_cnpj(valid_cnpj):
    mock_session = MagicMock()
    repo = RuralProducerRepository()

    producer_data = RuralProducerCreate(name="Test", document_type="CNPJ", document=valid_cnpj)
    producer = repo.create(mock_session, producer_data)

    assert producer.name == "Test"
    assert producer.document_type == "CNPJ"
    assert producer.document == "72249686000160"
    mock_session.add.assert_called_once_with(producer)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(producer)

def test_create_rural_producer_with_invalid_cnpj_should_return_error(invalid_cnpj):

    with pytest.raises(ValidationError) as exc_info:
        RuralProducerCreate(
            name="Test",
            document_type="CNPJ",
            document=invalid_cnpj
        )

    assert "Invalid CNPJ" in str(exc_info.value)

def test_get_all_producers(valid_cpf, valid_cnpj):
    mock_session = MagicMock()
    repo = RuralProducerRepository()

    expected_producers = [
        RuralProducer(id=uuid4(), name="Test", document_type="CPF", document=valid_cpf),
        RuralProducer(id=uuid4(), name="Teste2", document_type="CNPJ", document=valid_cnpj)
    ]
    mock_session.query.return_value.all.return_value = expected_producers

    result = repo.get_all(mock_session)

    assert result == expected_producers
    mock_session.query.assert_called_once_with(RuralProducer)
    mock_session.query.return_value.all.assert_called_once()

def test_update_rural_producer_success():
    mock_session = MagicMock()
    repo = RuralProducerRepository()

    rural_producer_id = uuid4()
    existing_rural_producer = RuralProducer(id=rural_producer_id, name="Juarez")
    repo.get_by_id = MagicMock(return_value=existing_rural_producer)

    update_data = RuralProducerUpdate(name="Juca")

    updated_rural_producer = repo.update(mock_session, rural_producer_id, update_data)

    assert updated_rural_producer.name == "Juca"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(existing_rural_producer)

def test_update_rural_producer_not_found():
    mock_session = MagicMock()
    repo = RuralProducerRepository()

    rural_producer_id = uuid4()
    repo.get_by_id = MagicMock(return_value=None)

    update_data = RuralProducer(name="Bean")
    result = repo.update(mock_session, rural_producer_id, update_data)

    assert result is None
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


def test_delete_rural_producer_success():
    mock_session = MagicMock()
    repo = RuralProducerRepository()

    rural_producer_id = uuid4()
    rural_producer = RuralProducer(id=rural_producer_id, name="wheat")
    repo.get_by_id = MagicMock(return_value=rural_producer)

    result = repo.delete(mock_session, rural_producer_id)

    assert result is True
    mock_session.delete.assert_called_once_with(rural_producer)
    mock_session.commit.assert_called_once()