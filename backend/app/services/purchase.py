from sqlalchemy.orm import Session

from app.constants.enums import PurchaseStrategy
from app.core.exceptions import AppException
from app.models.base import generate_prefixed_id
from app.models.purchase_plan import PurchasePlan
from app.models.user import User
from app.mock_data.demo_data import PRODUCT_CATALOG
from app.repositories.purchase import PurchasePlanRepository
from app.schemas.purchase import (
    CheckoutRedirectData,
    CheckoutRedirectRequest,
    ProductMatchData,
    ProductMatchItem,
    ProductMatchRequest,
    PurchasePlanData,
    PurchasePlanItem,
    PurchasePlanRecipe,
    PurchasePlanRequest,
    TakeoutAlternative,
)
from app.services.recipe import RecipeService
from app.schemas.recipe import MissingAnalysisRequest


class PurchaseService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.plan_repo = PurchasePlanRepository(db)
        self.recipe_service = RecipeService(db)

    def _estimate_product(self, ingredient_base_id: str | None, ingredient_name: str) -> dict:
        if ingredient_base_id and ingredient_base_id in PRODUCT_CATALOG:
            return PRODUCT_CATALOG[ingredient_base_id][0]
        for products in PRODUCT_CATALOG.values():
            for product in products:
                if ingredient_name in product["product_name"]:
                    return product
        return {
            "product_id": generate_prefixed_id("prd"),
            "product_name": f"{ingredient_name} 标准装",
            "price": 9.9,
            "original_price": 11.9,
            "discount_text": "演示价",
            "merchant_name": "美团精选商家",
            "eta_minutes": 35,
        }

    def create_plan(self, user: User, payload: PurchasePlanRequest) -> PurchasePlanData:
        analysis = self.recipe_service.analyze_missing(user, MissingAnalysisRequest(recipe_ids=payload.recipe_ids, servings=2))
        items: list[PurchasePlanItem] = []
        estimated_total = 0.0
        for missing in analysis.aggregated_missing:
            estimate = self._estimate_product(missing.ingredient_base_id, missing.ingredient_name)
            estimated_total += float(estimate["price"])
            items.append(
                PurchasePlanItem(
                    ingredient_base_id=missing.ingredient_base_id,
                    ingredient_name=missing.ingredient_name,
                    required_quantity=missing.missing_quantity,
                    unit=missing.unit,
                    estimated_price=float(estimate["price"]),
                    reason="核心主料缺失" if missing.ingredient_base_id in {"ing_beef", "ing_chicken"} else "补齐即可完成菜谱",
                )
            )

        recipes = [PurchasePlanRecipe(recipe_id=recipe.recipe_id, recipe_name=recipe.recipe_name) for recipe in analysis.recipes]
        promotion_explanation = (
            "当前方案优先选择刚好够用的小规格，减少浪费"
            if payload.strategy == PurchaseStrategy.LOWEST_COST.value
            else "当前方案优先减少商品件数，方便爸妈一键下单"
        )
        plan = PurchasePlan(
            id=generate_prefixed_id("plan"),
            user_id=user.id,
            household_id=user.household_id,
            strategy=payload.strategy,
            recipe_ids=payload.recipe_ids,
            aggregated_missing=[item.model_dump() for item in analysis.aggregated_missing],
            estimated_total_price=round(estimated_total, 2),
            promotion_explanation=promotion_explanation,
        )
        saved = self.plan_repo.create(plan)
        return PurchasePlanData(
            plan_id=saved.id,
            strategy=saved.strategy,
            recipes=recipes,
            items=items,
            promotion_explanation=saved.promotion_explanation,
            estimated_total_price=float(saved.estimated_total_price),
        )

    def match_products(self, user: User, payload: ProductMatchRequest) -> ProductMatchData:
        plan = self.plan_repo.get_by_id(payload.plan_id)
        if plan is None or plan.user_id != user.id:
            raise AppException(code=40400, message="purchase plan not found", status_code=404)

        products: list[ProductMatchItem] = []
        for missing in plan.aggregated_missing:
            estimate = self._estimate_product(missing.get("ingredient_base_id"), missing["ingredient_name"])
            products.append(
                ProductMatchItem(
                    ingredient_base_id=missing.get("ingredient_base_id"),
                    ingredient_name=missing["ingredient_name"],
                    matched_product_id=estimate["product_id"],
                    product_name=estimate["product_name"],
                    price=float(estimate["price"]),
                    original_price=float(estimate["original_price"]),
                    discount_text=estimate["discount_text"],
                    merchant_name=estimate["merchant_name"],
                    eta_minutes=int(estimate["eta_minutes"]),
                )
            )

        takeout_alternatives = [
            TakeoutAlternative(
                merchant_id=item["merchant_id"],
                merchant_name=item["merchant_name"],
                dish_name=item["dish_name"],
                price=float(item["price"]),
                eta_minutes=int(item["eta_minutes"]),
                reason=item["reason"],
            )
            for item in self.recipe_service.get_takeout_alternatives(plan.recipe_ids)
        ]
        return ProductMatchData(plan_id=plan.id, products=products, takeout_alternatives=takeout_alternatives)

    def build_checkout_redirect(self, user: User, payload: CheckoutRedirectRequest) -> CheckoutRedirectData:
        delegate_enabled = payload.senior_mode_delegate_pay or user.senior_mode_enabled
        return CheckoutRedirectData(
            checkout_url=f"https://mock.meituan.com/checkout/{generate_prefixed_id('co')}",
            delegate_pay={
                "enabled": delegate_enabled,
                "share_message": "妈，今晚做饭差几样菜，我已经帮你选好了，点这里让孩子代付。"
                if delegate_enabled
                else "下单后可继续在 App 内完成支付。",
            },
        )
