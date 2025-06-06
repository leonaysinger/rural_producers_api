from datetime import datetime
from uuid import uuid4

from app.domain.models.user import User


def mock_user(
    name="test",
    email="test@teste.com",
    password_hash="$2b$12$mockedhash",
    is_active=True,
    created_at=None,
    updated_at=None,
) -> User:
    return User(
        id=id or uuid4(),
        name=name,
        email=email,
        password_hash=password_hash,
        is_active=is_active,
        created_at=created_at or datetime.utcnow(),
        updated_at=updated_at or datetime.utcnow(),
    )
