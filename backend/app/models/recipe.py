from sqlalchemy import Boolean, ForeignKey, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import StringPrimaryKeyMixin, TimestampMixin


class RecipeBase(Base, StringPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "recipe_base"

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    cook_time_minutes: Mapped[int] = mapped_column(nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)
    servings: Mapped[int] = mapped_column(nullable=False)
    cover_image: Mapped[str] = mapped_column(String(255), nullable=False)
    steps: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    takeout_keywords: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    ingredients = relationship("RecipeIngredientRel", back_populates="recipe")


class RecipeIngredientRel(Base, TimestampMixin):
    __tablename__ = "recipe_ingredient_rel"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    recipe_id: Mapped[str] = mapped_column(ForeignKey("recipe_base.id"), nullable=False, index=True)
    ingredient_base_id: Mapped[str | None] = mapped_column(ForeignKey("ingredient_base.id"), nullable=True, index=True)
    ingredient_name: Mapped[str] = mapped_column(String(100), nullable=False)
    required_quantity: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    optional: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    recipe = relationship("RecipeBase", back_populates="ingredients")
    ingredient_base = relationship("IngredientBase")

