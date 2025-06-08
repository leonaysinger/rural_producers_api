import os
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from app.domain.schemas.auth import LoginInput
from app.repositories import user_token as token_repo
from app.repositories.user import UserRepository


SECRET_KEY = os.getenv("SECRET_KEY", "fallback-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class AuthService:
    @staticmethod
    def login(db: Session, credentials: LoginInput) -> dict:
        user_repo = UserRepository()
        db_user = user_repo.get_by_email(db, credentials.email)

        if not db_user or not bcrypt.verify(credentials.password, db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        payload = {"sub": str(db_user.id), "email": db_user.email}

        access_token = AuthService.create_access_token(payload)
        refresh_token = AuthService.create_refresh_token(payload)

        access_exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_exp = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

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

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
