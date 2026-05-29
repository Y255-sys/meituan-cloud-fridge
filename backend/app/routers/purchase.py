from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ApiResponse, build_success
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.purchase import (
    CheckoutRedirectData,
    CheckoutRedirectRequest,
    ProductMatchData,
    ProductMatchRequest,
    PurchasePlanData,
    PurchasePlanRequest,
)
from app.services.purchase import PurchaseService

router = APIRouter(tags=["purchase"])


@router.post("/purchase-plans", response_model=ApiResponse[PurchasePlanData])
def create_purchase_plan(
    payload: PurchasePlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[PurchasePlanData]:
    data = PurchaseService(db).create_plan(current_user, payload)
    return build_success(data)


@router.post("/products/match", response_model=ApiResponse[ProductMatchData])
def match_products(
    payload: ProductMatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[ProductMatchData]:
    data = PurchaseService(db).match_products(current_user, payload)
    return build_success(data)


@router.post("/checkout/redirect", response_model=ApiResponse[CheckoutRedirectData])
def checkout_redirect(
    payload: CheckoutRedirectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[CheckoutRedirectData]:
    data = PurchaseService(db).build_checkout_redirect(current_user, payload)
    return build_success(data)

