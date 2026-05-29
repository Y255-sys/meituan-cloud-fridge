from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.constants.enums import InventorySourceType, StorageLocation
from app.core.exceptions import AppException
from app.models.base import generate_prefixed_id
from app.models.ingredient import UserIngredient
from app.models.order_sync import OrderSyncRel
from app.models.user import User
from app.mock_data.demo_data import MOCK_ORDERS
from app.repositories.ingredient import IngredientRepository
from app.repositories.order_sync import OrderSyncRepository
from app.schemas.order_sync import OrderSyncData, OrderSyncRequest


class OrderSyncService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.order_repo = OrderSyncRepository(db)
        self.ingredient_repo = IngredientRepository(db)

    def sync_order(self, user: User, payload: OrderSyncRequest) -> OrderSyncData:
        if self.order_repo.get_by_external_order_id(user.id, payload.external_order_id):
            raise AppException(code=40900, message="order already synced", status_code=409)

        order_payload = MOCK_ORDERS.get(payload.external_order_id)
        if order_payload is None:
            raise AppException(code=40400, message="mock order not found", status_code=404)

        imported_items = 0
        for item in order_payload["items"]:
            ingredient = self.ingredient_repo.get_by_id(item["ingredient_base_id"])
            expire_days = ingredient.default_expire_days if ingredient else 3
            storage_location = ingredient.storage_location if ingredient else StorageLocation.CHILLED.value
            category = ingredient.category if ingredient else "其他"
            self.db.add(
                UserIngredient(
                    id=generate_prefixed_id("ui"),
                    user_id=user.id,
                    household_id=user.household_id,
                    ingredient_base_id=item["ingredient_base_id"],
                    ingredient_name=item["ingredient_name"],
                    category=category,
                    quantity=item["quantity"],
                    unit=item["unit"],
                    storage_location=storage_location,
                    expire_at=date.today() + timedelta(days=expire_days),
                    status="fresh",
                    source_type=InventorySourceType.ORDER_SYNC.value,
                    source_ref_id=payload.external_order_id,
                    notes="订单同步入库",
                )
            )
            imported_items += 1

        order_record = OrderSyncRel(
            id=generate_prefixed_id("ord"),
            user_id=user.id,
            household_id=user.household_id,
            channel=payload.channel,
            external_order_id=payload.external_order_id,
            raw_payload=order_payload,
            sync_status="synced",
            imported_count=imported_items,
        )
        self.db.add(order_record)
        self.db.commit()
        self.db.refresh(order_record)
        return OrderSyncData(synced=True, order_id=order_record.id, imported_items=imported_items)

