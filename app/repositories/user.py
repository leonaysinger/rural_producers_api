from uuid import UUID

from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.domain.models.user import User
from app.domain.schemas.user import UserCreate, UserUpdate
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: EmailStr):
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user_in: UserCreate):
        db_user = User(
            name=user_in.name,
            email=user_in.email,
            password_hash=bcrypt.hash(user_in.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_user(self, db: Session, user_id: UUID, user_in: UserUpdate):
        user = self.get_by_id(db, user_id)
        if not user:
            return None

        if user_in.email is not None:
            user.email = user_in.email
        if user_in.name is not None:
            user.name = user_in.name
        if user_in.password is not None:
            user.hashed_password = bcrypt.hash(user_in.password)

        db.commit()
        db.refresh(user)
        return user
