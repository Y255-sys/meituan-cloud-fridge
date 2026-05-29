from app.schemas.common import AppBaseModel


class PurchasePlanRequest(AppBaseModel):
    recipe_ids: list[str]
    strategy: str = "lowest_cost"


class PurchasePlanRecipe(AppBaseModel):
    recipe_id: str
    recipe_name: str


class PurchasePlanItem(AppBaseModel):
    ingredient_base_id: str | None
    ingredient_name: str
    required_quantity: float
    unit: str
    estimated_price: float
    reason: str


class PurchasePlanData(AppBaseModel):
    plan_id: str
    strategy: str
    recipes: list[PurchasePlanRecipe]
    items: list[PurchasePlanItem]
    promotion_explanation: str
    estimated_total_price: float


class ProductMatchRequest(AppBaseModel):
    plan_id: str


class ProductMatchItem(AppBaseModel):
    ingredient_base_id: str | None
    ingredient_name: str
    matched_product_id: str
    product_name: str
    price: float
    original_price: float
    discount_text: str
    merchant_name: str
    eta_minutes: int


class TakeoutAlternative(AppBaseModel):
    merchant_id: str
    merchant_name: str
    dish_name: str
    price: float
    eta_minutes: int
    reason: str


class ProductMatchData(AppBaseModel):
    plan_id: str
    products: list[ProductMatchItem]
    takeout_alternatives: list[TakeoutAlternative]


class CheckoutRedirectRequest(AppBaseModel):
    source_type: str
    selected_product_ids: list[str]
    senior_mode_delegate_pay: bool = False


class CheckoutRedirectData(AppBaseModel):
    checkout_url: str
    delegate_pay: dict[str, bool | str]

