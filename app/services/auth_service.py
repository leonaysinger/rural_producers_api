import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from app.domain.schemas.auth import LoginInput
from app.repositories import user_token as token_repo
from app.repositories.user import UserRepository


class AuthService:
    @staticmethod
    def login(db: Session, credentials: LoginInput) -> dict:
        user_repo = UserRepository()
        db_user = user_repo.get_by_email(db, credentials.email)
        if not db_user or not bcrypt.verify(credentials.password,
                                            db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access_token = str(uuid.uuid4())
        refresh_token = str(uuid.uuid4())
        access_exp = datetime.utcnow() + timedelta(minutes=30)
        refresh_exp = datetime.utcnow() + timedelta(days=7)

        token_repo.create_token(
            db=db,
            user_id=db_user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=access_exp,
            refresh_expires_at=refresh_exp
        )

        return {
            "user_name": db_user.name,
            "user_email": db_user.email,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
