from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.constants.enums import InventorySourceType, InventoryStatus
from app.core.exceptions import AppException
from app.models.base import generate_prefixed_id
from app.models.ingredient import UserIngredient
from app.models.user import User
from app.repositories.ingredient import IngredientRepository
from app.repositories.inventory import InventoryRepository
from app.repositories.recognition import RecognitionRepository
from app.schemas.inventory import (
    ImportRecognitionData,
    ImportRecognitionRequest,
    InventoryCreateRequest,
    InventoryItem,
    InventoryListData,
    InventorySummary,
    InventoryUpdateRequest,
)


class InventoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.inventory_repo = InventoryRepository(db)
        self.ingredient_repo = IngredientRepository(db)
        self.recognition_repo = RecognitionRepository(db)

    @staticmethod
    def _to_float(value: Decimal | float | int | None) -> float:
        return float(value) if value is not None else 0.0

    @staticmethod
    def _compute_status(expire_at: date | None) -> str:
        if expire_at is None:
            return InventoryStatus.FRESH.value
        delta_days = (expire_at - date.today()).days
        if delta_days < 0:
            return InventoryStatus.EXPIRED.value
        if delta_days <= 2:
            return InventoryStatus.EXPIRING.value
        return InventoryStatus.FRESH.value

    @staticmethod
    def _days_to_expire(expire_at: date | None) -> int | None:
        if expire_at is None:
            return None
        return (expire_at - date.today()).days

    def _resolve_category(self, ingredient_base_id: str | None, ingredient_name: str, category: str | None = None) -> str:
        if category:
            return category
        if ingredient_base_id:
            ingredient = self.ingredient_repo.get_by_id(ingredient_base_id)
            if ingredient:
                return ingredient.category
        ingredient = self.ingredient_repo.get_by_name(ingredient_name)
        if ingredient:
            return ingredient.category
        return "其他"

    def _serialize_item(self, item: UserIngredient) -> InventoryItem:
        return InventoryItem(
            id=item.id,
            ingredient_base_id=item.ingredient_base_id,
            ingredient_name=item.ingredient_name,
            category=item.category,
            quantity=self._to_float(item.quantity),
            unit=item.unit,
            storage_location=item.storage_location,
            status=item.status,
            expire_at=item.expire_at,
            days_to_expire=self._days_to_expire(item.expire_at),
            source_type=item.source_type,
            source_ref_id=item.source_ref_id,
            updated_at=item.updated_at,
        )

    def _build_summary(self, items: list[UserIngredient]) -> InventorySummary:
        expiring_count = sum(1 for item in items if item.status == InventoryStatus.EXPIRING.value)
        expired_count = sum(1 for item in items if item.status == InventoryStatus.EXPIRED.value)
        return InventorySummary(
            total_items=len(items),
            expiring_items=expiring_count,
            expired_items=expired_count,
        )

    def list_inventory(
        self,
        user: User,
        keyword: str | None = None,
        category: str | None = None,
        status: str | None = None,
        storage_location: str | None = None,
        sort_by: str | None = None,
    ) -> InventoryListData:
        items = self.inventory_repo.list_items(
            household_id=user.household_id,
            keyword=keyword,
            category=category,
            status=status,
            storage_location=storage_location,
            sort_by=sort_by,
        )
        for item in items:
            item.status = self._compute_status(item.expire_at)
        serialized = [self._serialize_item(item) for item in items]
        return InventoryListData(summary=self._build_summary(items), items=serialized)

    def get_item(self, user: User, item_id: str) -> InventoryItem:
        item = self.inventory_repo.get_by_id(item_id)
        if item is None or item.household_id != user.household_id:
            raise AppException(code=40400, message="inventory item not found", status_code=404)
        item.status = self._compute_status(item.expire_at)
        return self._serialize_item(item)

    def create_item(self, user: User, payload: InventoryCreateRequest) -> InventoryItem:
        item = UserIngredient(
            id=generate_prefixed_id("ui"),
            user_id=user.id,
            household_id=user.household_id,
            ingredient_base_id=payload.ingredient_base_id,
            ingredient_name=payload.ingredient_name,
            category=self._resolve_category(payload.ingredient_base_id, payload.ingredient_name, payload.category),
            quantity=payload.quantity,
            unit=payload.unit,
            storage_location=payload.storage_location,
            expire_at=payload.expire_at,
            status=self._compute_status(payload.expire_at),
            source_type=InventorySourceType.MANUAL.value,
            source_ref_id=None,
            notes=payload.notes,
        )
        created = self.inventory_repo.create(item)
        return self._serialize_item(created)

    def update_item(self, user: User, item_id: str, payload: InventoryUpdateRequest) -> InventoryItem:
        item = self.inventory_repo.get_by_id(item_id)
        if item is None or item.household_id != user.household_id:
            raise AppException(code=40400, message="inventory item not found", status_code=404)
        updates = payload.model_dump(exclude_unset=True)
        for field_name, value in updates.items():
            setattr(item, field_name, value)
        item.category = self._resolve_category(item.ingredient_base_id, item.ingredient_name, item.category)
        item.status = self._compute_status(item.expire_at)
        updated = self.inventory_repo.update(item)
        return self._serialize_item(updated)

    def delete_item(self, user: User, item_id: str) -> dict[str, bool]:
        item = self.inventory_repo.get_by_id(item_id)
        if item is None or item.household_id != user.household_id:
            raise AppException(code=40400, message="inventory item not found", status_code=404)
        self.inventory_repo.delete(item)
        return {"deleted": True}

    def import_recognition(self, user: User, payload: ImportRecognitionRequest) -> ImportRecognitionData:
        record = self.recognition_repo.get_by_id(payload.recognition_id)
        if record is None or record.user_id != user.id:
            raise AppException(code=40400, message="recognition record not found", status_code=404)

        items_to_create: list[UserIngredient] = []
        for entry in payload.items:
            items_to_create.append(
                UserIngredient(
                    id=generate_prefixed_id("ui"),
                    user_id=user.id,
                    household_id=user.household_id,
                    ingredient_base_id=entry.ingredient_base_id,
                    ingredient_name=entry.ingredient_name,
                    category=self._resolve_category(entry.ingredient_base_id, entry.ingredient_name),
                    quantity=entry.quantity,
                    unit=entry.unit,
                    storage_location=entry.storage_location,
                    expire_at=entry.expire_at,
                    status=self._compute_status(entry.expire_at),
                    source_type=InventorySourceType.RECOGNITION.value,
                    source_ref_id=payload.recognition_id,
                    notes=None,
                )
            )

        self.inventory_repo.bulk_create(items_to_create)
        inventory = self.list_inventory(user)
        return ImportRecognitionData(imported_count=len(items_to_create), summary=inventory.summary)

