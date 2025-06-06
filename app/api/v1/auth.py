from fastapi import APIRouter

from app.core.dependencies import DBSession
from app.domain.schemas.auth import LoginInput
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login")
def login(credentials: LoginInput, db: DBSession):
    return AuthService.login(db, credentials)
