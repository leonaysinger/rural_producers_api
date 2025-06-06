from unittest.mock import MagicMock
from uuid import uuid4

from app.domain.models.user import User
from app.domain.schemas.user import UserCreate, UserUpdate
from app.repositories.user import UserRepository


def test_create_user():
    mock_session = MagicMock()
    repo = UserRepository()
    user_data = UserCreate(name="João", email="joao@mail.com", password="abc123")

    user = repo.create(mock_session, user_data)

    assert user.name == "João"
    assert user.email == "joao@mail.com"
    assert user.password_hash != "abc123"
    assert user.password_hash.startswith("$2b$")
    mock_session.add.assert_called_once_with(user)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(user)


def test_list_users(mock_user_model):
    mock_session = MagicMock()
    repo = UserRepository()

    query_mock = MagicMock()
    query_mock.all.return_value = [mock_user_model]
    mock_session.query.return_value = query_mock

    result = repo.get_all(mock_session)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == mock_user_model
    mock_session.query.assert_called_once_with(User)
    query_mock.all.assert_called_once()


def test_get_by_email(mock_user_model):
    mock_session = MagicMock()
    repo = UserRepository()

    query_mock = MagicMock()
    filter_mock = MagicMock()
    filter_mock.first.return_value = mock_user_model
    query_mock.filter.return_value = filter_mock
    mock_session.query.return_value = query_mock

    result = repo.get_by_email(mock_session, mock_user_model.email)

    assert result == mock_user_model
    mock_session.query.assert_called_once_with(User)
    query_mock.filter.assert_called_once()
    filter_mock.first.assert_called_once()


def test_update_user_success(mock_user_model):
    mock_session = MagicMock()
    repo = UserRepository()
    user_id = mock_user_model.id

    repo.get_by_id = MagicMock(return_value=mock_user_model)

    update_data = UserUpdate(
        name="Novo Nome", email="novo@mail.com", password="novaSenha123"
    )

    updated_user = repo.update_user(mock_session, user_id, update_data)

    assert updated_user.name == "Novo Nome"
    assert updated_user.email == "novo@mail.com"
    assert updated_user.hashed_password.startswith("$2b$")
    assert updated_user.hashed_password != "novaSenha123"

    repo.get_by_id.assert_called_once_with(mock_session, user_id)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_user_model)


def test_update_user_not_found():
    mock_session = MagicMock()
    repo = UserRepository()
    fake_user_id = uuid4()

    repo.get_by_id = MagicMock(return_value=None)

    update_data = UserUpdate(name="Novo Nome")
    result = repo.update_user(mock_session, fake_user_id, update_data)

    assert result is None
    repo.get_by_id.assert_called_once_with(mock_session, fake_user_id)
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


def test_deactivate_user_success(mock_user_model):
    mock_session = MagicMock()
    from app.repositories.user import UserRepository

    repo = UserRepository()

    query_mock = MagicMock()
    query_mock.filter.return_value.first.return_value = mock_user_model
    mock_session.query.return_value = query_mock

    result = repo.deactivate(mock_session, str(mock_user_model.id))

    assert result is True
    assert mock_user_model.is_active is False
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_user_model)
