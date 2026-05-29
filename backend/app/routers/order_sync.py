from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ApiResponse, build_success
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.order_sync import OrderSyncData, OrderSyncRequest
from app.services.order_sync import OrderSyncService

router = APIRouter(tags=["order-sync"])


@router.post("/order-sync", response_model=ApiResponse[OrderSyncData])
def sync_order(
    payload: OrderSyncRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[OrderSyncData]:
    data = OrderSyncService(db).sync_order(current_user, payload)
    return build_success(data)

