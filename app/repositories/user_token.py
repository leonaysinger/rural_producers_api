from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.models.user_token import UserToken


def create_token(
    db: Session,
    user_id: UUID,
    access_token: str,
    refresh_token: str,
    expires_at: datetime,
    refresh_expires_at: datetime
) -> UserToken:
    db_token = UserToken(
        user_id=user_id,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
        refresh_expires_at=refresh_expires_at
    )

    try:
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        return db_token
    except Exception as e:
        db.rollback()
        raise e
