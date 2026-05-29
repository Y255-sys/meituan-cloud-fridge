from sqlalchemy import ForeignKey, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import StringPrimaryKeyMixin, TimestampMixin


class PurchasePlan(Base, StringPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "purchase_plan"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    household_id: Mapped[str] = mapped_column(ForeignKey("households.id"), nullable=False, index=True)
    strategy: Mapped[str] = mapped_column(String(30), nullable=False)
    recipe_ids: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    aggregated_missing: Mapped[list[dict]] = mapped_column(JSON, default=list, nullable=False)
    estimated_total_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    promotion_explanation: Mapped[str] = mapped_column(String(255), nullable=False)

