from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order_sync import OrderSyncRel


class OrderSyncRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_external_order_id(self, user_id: str, external_order_id: str) -> OrderSyncRel | None:
        query = select(OrderSyncRel).where(
            OrderSyncRel.user_id == user_id,
            OrderSyncRel.external_order_id == external_order_id,
        )
        return self.db.scalar(query)

    def create(self, record: OrderSyncRel) -> OrderSyncRel:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

