from datetime import date

from sqlalchemy import Date, ForeignKey, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import StringPrimaryKeyMixin, TimestampMixin


class IngredientBase(Base, StringPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "ingredient_base"

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    default_unit: Mapped[str] = mapped_column(String(20), nullable=False)
    default_expire_days: Mapped[int] = mapped_column(nullable=False)
    storage_location: Mapped[str] = mapped_column(String(20), nullable=False)
    searchable_keywords: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)


class UserIngredient(Base, StringPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "user_ingredient"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    household_id: Mapped[str] = mapped_column(ForeignKey("households.id"), nullable=False, index=True)
    ingredient_base_id: Mapped[str | None] = mapped_column(ForeignKey("ingredient_base.id"), nullable=True, index=True)
    ingredient_name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    storage_location: Mapped[str] = mapped_column(String(20), nullable=False)
    expire_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String(20), nullable=False)
    source_ref_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user = relationship("User", back_populates="inventory_items")
    household = relationship("Household", back_populates="inventory_items")
    ingredient_base = relationship("IngredientBase")

