from sqlalchemy import Boolean, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import StringPrimaryKeyMixin, TimestampMixin


class User(Base, StringPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False)
    household_id: Mapped[str | None] = mapped_column(ForeignKey("households.id"), nullable=True, index=True)
    senior_mode_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    city_code: Mapped[str] = mapped_column(String(20), default="310100", nullable=False)
    dietary_preferences: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    allergy_tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    taste_tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    household = relationship("Household", back_populates="users", foreign_keys=[household_id])
    inventory_items = relationship("UserIngredient", back_populates="user")
    recognitions = relationship("RecognitionRecord", back_populates="user")
