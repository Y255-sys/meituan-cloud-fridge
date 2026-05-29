from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import StringPrimaryKeyMixin, TimestampMixin


class OrderSyncRel(Base, StringPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "order_sync_rel"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    household_id: Mapped[str] = mapped_column(ForeignKey("households.id"), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    external_order_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    sync_status: Mapped[str] = mapped_column(String(20), nullable=False)
    imported_count: Mapped[int] = mapped_column(nullable=False)

