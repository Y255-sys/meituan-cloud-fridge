from datetime import date, datetime

from pydantic import Field

from app.schemas.common import AppBaseModel


class InventorySummary(AppBaseModel):
    total_items: int
    expiring_items: int
    expired_items: int


class InventoryItem(AppBaseModel):
    id: str
    ingredient_base_id: str | None
    ingredient_name: str
    category: str
    quantity: float
    unit: str
    storage_location: str
    status: str
    expire_at: date | None
    days_to_expire: int | None
    source_type: str
    source_ref_id: str | None
    updated_at: datetime


class InventoryListData(AppBaseModel):
    summary: InventorySummary
    items: list[InventoryItem]


class InventoryCreateRequest(AppBaseModel):
    ingredient_base_id: str | None = None
    ingredient_name: str = Field(min_length=1, max_length=100)
    category: str | None = None
    quantity: float = Field(gt=0)
    unit: str = Field(min_length=1, max_length=20)
    storage_location: str = Field(min_length=1, max_length=20)
    expire_at: date | None = None
    notes: str | None = None


class InventoryUpdateRequest(AppBaseModel):
    ingredient_name: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = None
    quantity: float | None = Field(default=None, gt=0)
    unit: str | None = Field(default=None, min_length=1, max_length=20)
    storage_location: str | None = Field(default=None, min_length=1, max_length=20)
    expire_at: date | None = None
    notes: str | None = None


class ImportRecognitionItemRequest(AppBaseModel):
    ingredient_base_id: str | None = None
    ingredient_name: str = Field(min_length=1, max_length=100)
    quantity: float = Field(gt=0)
    unit: str = Field(min_length=1, max_length=20)
    storage_location: str = Field(min_length=1, max_length=20)
    expire_at: date | None = None


class ImportRecognitionRequest(AppBaseModel):
    recognition_id: str
    items: list[ImportRecognitionItemRequest]


class ImportRecognitionData(AppBaseModel):
    imported_count: int
    summary: InventorySummary
