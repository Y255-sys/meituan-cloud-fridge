from sqlalchemy.orm import Session

from app.models.recognition import RecognitionRecord


class RecognitionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, record: RecognitionRecord) -> RecognitionRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_by_id(self, recognition_id: str) -> RecognitionRecord | None:
        return self.db.get(RecognitionRecord, recognition_id)

