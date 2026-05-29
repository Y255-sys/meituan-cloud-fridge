from app.schemas.common import AppBaseModel


class RecipeCard(AppBaseModel):
    recipe_id: str
    recipe_name: str
    cover_image: str
    cook_time_minutes: int
    match_score: int
    missing_count: int
    highlight_reason: str


class RecommendationGroup(AppBaseModel):
    type: str
    title: str
    description: str
    recipes: list[RecipeCard]


class RecipeRecommendationsData(AppBaseModel):
    context: dict[str, str | int]
    groups: list[RecommendationGroup]


class RecipeIngredientUsage(AppBaseModel):
    ingredient_base_id: str | None
    ingredient_name: str
    required_quantity: float
    unit: str
    owned_quantity: float
    missing_quantity: float


class RecipeDetail(AppBaseModel):
    recipe_id: str
    recipe_name: str
    description: str
    cook_time_minutes: int
    difficulty: str
    servings: int
    steps: list[str]
    ingredients: list[RecipeIngredientUsage]
    nutrition_tip: str
    can_cook_now: bool


class MissingIngredient(AppBaseModel):
    ingredient_base_id: str | None
    ingredient_name: str
    missing_quantity: float
    unit: str


class MissingAnalysisRecipe(AppBaseModel):
    recipe_id: str
    recipe_name: str
    missing_ingredients: list[MissingIngredient]


class MissingAnalysisRequest(AppBaseModel):
    recipe_ids: list[str]
    servings: int = 2


class MissingAnalysisData(AppBaseModel):
    recipes: list[MissingAnalysisRecipe]
    aggregated_missing: list[MissingIngredient]

