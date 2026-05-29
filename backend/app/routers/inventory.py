from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ApiResponse, build_success
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.inventory import (
    ImportRecognitionData,
    ImportRecognitionRequest,
    InventoryCreateRequest,
    InventoryItem,
    InventoryListData,
    InventoryUpdateRequest,
)
from app.services.inventory import InventoryService

router = APIRouter(tags=["inventory"])


@router.get("/inventory", response_model=ApiResponse[InventoryListData])
def list_inventory(
    keyword: str | None = None,
    category: str | None = None,
    status: str | None = None,
    storage_location: str | None = None,
    sort_by: str | None = Query(default="expire_at"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[InventoryListData]:
    data = InventoryService(db).list_inventory(current_user, keyword, category, status, storage_location, sort_by)
    return build_success(data)


@router.post("/inventory", response_model=ApiResponse[InventoryItem])
def create_inventory_item(
    payload: InventoryCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[InventoryItem]:
    data = InventoryService(db).create_item(current_user, payload)
    return build_success(data)


@router.get("/inventory/{item_id}", response_model=ApiResponse[InventoryItem])
def get_inventory_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[InventoryItem]:
    data = InventoryService(db).get_item(current_user, item_id)
    return build_success(data)


@router.patch("/inventory/{item_id}", response_model=ApiResponse[InventoryItem])
def update_inventory_item(
    item_id: str,
    payload: InventoryUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[InventoryItem]:
    data = InventoryService(db).update_item(current_user, item_id, payload)
    return build_success(data)


@router.delete("/inventory/{item_id}", response_model=ApiResponse[dict[str, bool]])
def delete_inventory_item(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[dict[str, bool]]:
    data = InventoryService(db).delete_item(current_user, item_id)
    return build_success(data)


@router.post("/inventory/import-recognition", response_model=ApiResponse[ImportRecognitionData])
def import_recognition(
    payload: ImportRecognitionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[ImportRecognitionData]:
    data = InventoryService(db).import_recognition(current_user, payload)
    return build_success(data)

