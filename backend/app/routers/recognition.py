from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ApiResponse, build_success
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.recognition import RecognitionResult
from app.services.recognition import RecognitionService

router = APIRouter(tags=["recognition"])


@router.post("/recognitions", response_model=ApiResponse[RecognitionResult])
def create_recognition(
    image: UploadFile = File(...),
    scene: str = Form("fridge"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[RecognitionResult]:
    data = RecognitionService(db).recognize(current_user, image, scene)
    return build_success(data)

