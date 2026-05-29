from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import StringPrimaryKeyMixin, TimestampMixin


class Household(Base, StringPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "households"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    owner_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    users = relationship("User", back_populates="household", foreign_keys="User.household_id")
    inventory_items = relationship("UserIngredient", back_populates="household")
