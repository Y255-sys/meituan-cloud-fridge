from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ApiResponse, build_success
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.common import StatusToggleRequest
from app.services.profile import ProfileService

router = APIRouter(tags=["senior-mode"])


@router.patch("/profile/senior-mode", response_model=ApiResponse[dict[str, bool]])
def toggle_senior_mode(
    payload: StatusToggleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[dict[str, bool]]:
    data = ProfileService(db).toggle_senior_mode(current_user, payload.enabled)
    return build_success(data)

