from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ApiResponse, build_success
from app.schemas.auth import AuthPayload, LoginRequest, RegisterRequest
from app.services.auth import AuthService

router = APIRouter(tags=["auth"])


@router.post("/auth/register", response_model=ApiResponse[AuthPayload])
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> ApiResponse[AuthPayload]:
    data = AuthService(db).register(payload)
    return build_success(data)


@router.post("/auth/login", response_model=ApiResponse[AuthPayload])
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> ApiResponse[AuthPayload]:
    data = AuthService(db).login(payload)
    return build_success(data)

