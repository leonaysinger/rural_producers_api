import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.dependencies import DBSession
from app.domain.models.user import User
from app.domain.schemas.user import UserCreate, UserRead, UserUpdate
from app.repositories.user import UserRepository

router = APIRouter(prefix="/users")
logger = logging.getLogger(__name__)


@router.post("/", response_model=UserRead)
def create_user(new_user: UserCreate, db: DBSession) -> User:
    user_repo = UserRepository()
    user = user_repo.get_by_email(db, new_user.email)
    if user:
        logger.warning(f"User created error: duplicated email: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_repo.create(db, new_user)


@router.get("/", response_model=None)
def list_users(db: DBSession) -> list[User]:
    repo = UserRepository()
    return repo.get_all(db)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, db: DBSession) -> User:
    user_repo = UserRepository()
    user = user_repo.get_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: UUID, user_in: UserUpdate, db: DBSession) -> User:
    try:
        user_repo = UserRepository()
        user = user_repo.update_user(db, user_id, user_in)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered") from err
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error") from err


@router.delete("/{user_id}", response_model=bool)
def delete_user(user_id: UUID, db: DBSession) -> bool:
    user_repo = UserRepository()
    return user_repo.deactivate(db, user_id)
