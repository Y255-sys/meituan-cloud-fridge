from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ApiResponse, build_success
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.profile import UpdateProfileRequest, UserProfile
from app.services.profile import ProfileService

router = APIRouter(tags=["profile"])


@router.get("/profile", response_model=ApiResponse[UserProfile])
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[UserProfile]:
    data = ProfileService(db).get_profile(current_user)
    return build_success(data)


@router.patch("/profile", response_model=ApiResponse[UserProfile])
def update_profile(
    payload: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[UserProfile]:
    data = ProfileService(db).update_profile(current_user, payload)
    return build_success(data)

