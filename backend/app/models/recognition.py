from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import StringPrimaryKeyMixin, TimestampMixin


class RecognitionRecord(Base, StringPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "recognition_record"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    image_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    scene: Mapped[str] = mapped_column(String(50), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    result_payload: Mapped[list[dict]] = mapped_column(JSON, default=list, nullable=False)

    user = relationship("User", back_populates="recognitions")

