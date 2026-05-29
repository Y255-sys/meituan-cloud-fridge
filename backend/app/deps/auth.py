from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise AppException(code=40100, message="missing access token", status_code=401)

    try:
        payload = decode_access_token(credentials.credentials)
    except PyJWTError as exc:
        raise AppException(code=40100, message="invalid access token", status_code=401) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise AppException(code=40100, message="invalid access token", status_code=401)

    user = UserRepository(db).get_by_id(user_id)
    if user is None:
        raise AppException(code=40100, message="user not found", status_code=401)

    return user

