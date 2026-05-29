from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.base import generate_prefixed_id
from app.models.recognition import RecognitionRecord
from app.models.user import User
from app.mock_data.demo_data import RECOGNITION_PRESETS
from app.repositories.recognition import RecognitionRepository
from app.schemas.recognition import RecognitionItem, RecognitionResult


class RecognitionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.recognition_repo = RecognitionRepository(db)

    def recognize(self, user: User, image: UploadFile, scene: str) -> RecognitionResult:
        preset = RECOGNITION_PRESETS.get(scene) or RECOGNITION_PRESETS["fridge"]
        recognition_id = generate_prefixed_id("rec")
        items = [
            RecognitionItem(
                temp_id=generate_prefixed_id("tmp"),
                ingredient_base_id=item["ingredient_base_id"],
                ingredient_name=item["ingredient_name"],
                quantity=item["quantity"],
                unit=item["unit"],
                confidence=item["confidence"],
                source="vision_mock",
                editable=True,
                suggested_storage_location=item["suggested_storage_location"],
                suggested_expire_days=item["suggested_expire_days"],
            )
            for item in preset
        ]
        record = RecognitionRecord(
            id=recognition_id,
            user_id=user.id,
            image_filename=image.filename or "upload.jpg",
            scene=scene,
            image_url=f"/mock/recognition/{recognition_id}.jpg",
            result_payload=[item.model_dump() for item in items],
        )
        self.recognition_repo.create(record)
        return RecognitionResult(recognition_id=recognition_id, image_url=record.image_url, items=items)
