from collections import defaultdict
from decimal import Decimal

from sqlalchemy.orm import Session

from app.constants.enums import RecommendationGroupType
from app.core.exceptions import AppException
from app.models.recipe import RecipeBase, RecipeIngredientRel
from app.models.user import User
from app.mock_data.demo_data import TAKEOUT_ALTERNATIVES
from app.repositories.inventory import InventoryRepository
from app.repositories.recipe import RecipeRepository
from app.schemas.recipe import (
    MissingAnalysisData,
    MissingAnalysisRecipe,
    MissingAnalysisRequest,
    MissingIngredient,
    RecommendationGroup,
    RecipeCard,
    RecipeDetail,
    RecipeIngredientUsage,
    RecipeRecommendationsData,
)


class RecipeService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.recipe_repo = RecipeRepository(db)
        self.inventory_repo = InventoryRepository(db)

    @staticmethod
    def _to_float(value: Decimal | float | int | None) -> float:
        return float(value) if value is not None else 0.0

    def _inventory_map(self, household_id: str) -> dict[str, float]:
        inventory = self.inventory_repo.list_items(household_id=household_id, sort_by="updated_at")
        quantities: dict[str, float] = defaultdict(float)
        for item in inventory:
            key = item.ingredient_base_id or item.ingredient_name
            quantities[key] += self._to_float(item.quantity)
        return quantities

    def _calculate_missing(
        self,
        recipe: RecipeBase,
        inventory_map: dict[str, float],
        servings: int | None = None,
    ) -> tuple[list[RecipeIngredientUsage], int]:
        target_servings = servings or recipe.servings
        scale_ratio = target_servings / recipe.servings if recipe.servings else 1
        usages: list[RecipeIngredientUsage] = []
        missing_count = 0
        for ingredient in recipe.ingredients:
            required = self._to_float(ingredient.required_quantity) * scale_ratio
            key = ingredient.ingredient_base_id or ingredient.ingredient_name
            owned = inventory_map.get(key, 0.0)
            missing = max(required - owned, 0.0)
            if missing > 0 and not ingredient.optional:
                missing_count += 1
            usages.append(
                RecipeIngredientUsage(
                    ingredient_base_id=ingredient.ingredient_base_id,
                    ingredient_name=ingredient.ingredient_name,
                    required_quantity=round(required, 2),
                    unit=ingredient.unit,
                    owned_quantity=round(owned, 2),
                    missing_quantity=round(missing, 2),
                )
            )
        return usages, missing_count

    def get_recommendations(
        self,
        user: User,
        meal_type: str = "dinner",
        servings: int = 2,
        scene: str = "worker_evening",
    ) -> RecipeRecommendationsData:
        inventory_map = self._inventory_map(user.household_id)
        all_recipes = self.recipe_repo.list_all()

        cook_now_cards: list[RecipeCard] = []
        buy_little_cards: list[RecipeCard] = []
        takeout_cards: list[RecipeCard] = []

        for recipe in all_recipes:
            usages, missing_count = self._calculate_missing(recipe, inventory_map, servings)
            total_required = len([item for item in recipe.ingredients if not item.optional]) or 1
            matched_required = sum(
                1
                for ingredient, usage in zip(recipe.ingredients, usages, strict=False)
                if not ingredient.optional and usage.missing_quantity == 0
            )
            match_score = int((matched_required / total_required) * 100)
            card = RecipeCard(
                recipe_id=recipe.id,
                recipe_name=recipe.name,
                cover_image=recipe.cover_image,
                cook_time_minutes=recipe.cook_time_minutes,
                match_score=match_score,
                missing_count=missing_count,
                highlight_reason="优先消耗现有库存" if missing_count == 0 else f"仅差 {missing_count} 样核心食材",
            )
            if missing_count == 0:
                cook_now_cards.append(card)
            elif missing_count <= 2:
                buy_little_cards.append(card)

            if recipe.id in TAKEOUT_ALTERNATIVES:
                takeout_cards.append(
                    RecipeCard(
                        recipe_id=recipe.id,
                        recipe_name=TAKEOUT_ALTERNATIVES[recipe.id][0]["dish_name"],
                        cover_image=recipe.cover_image,
                        cook_time_minutes=TAKEOUT_ALTERNATIVES[recipe.id][0]["eta_minutes"],
                        match_score=max(match_score, 75),
                        missing_count=missing_count,
                        highlight_reason=TAKEOUT_ALTERNATIVES[recipe.id][0]["reason"],
                    )
                )

        cook_now_cards.sort(key=lambda item: (-item.match_score, item.cook_time_minutes))
        buy_little_cards.sort(key=lambda item: (item.missing_count, -item.match_score))
        takeout_cards.sort(key=lambda item: (-item.match_score, item.cook_time_minutes))

        return RecipeRecommendationsData(
            context={"meal_type": meal_type, "scene": scene, "inventory_count": len(inventory_map)},
            groups=[
                RecommendationGroup(
                    type=RecommendationGroupType.COOK_NOW.value,
                    title="不补购也能做",
                    description="优先消耗现有库存",
                    recipes=cook_now_cards[:3],
                ),
                RecommendationGroup(
                    type=RecommendationGroupType.BUY_LITTLE.value,
                    title="少量补购就能做",
                    description="差 1 到 2 样核心食材就能完成",
                    recipes=buy_little_cards[:3],
                ),
                RecommendationGroup(
                    type=RecommendationGroupType.TAKEOUT.value,
                    title="不想做饭，直接外卖替代",
                    description="给今晚一个省事的备选方案",
                    recipes=takeout_cards[:3],
                ),
            ],
        )

    def get_recipe_detail(self, user: User, recipe_id: str) -> RecipeDetail:
        recipe = self.recipe_repo.get_by_id(recipe_id)
        if recipe is None:
            raise AppException(code=40400, message="recipe not found", status_code=404)
        inventory_map = self._inventory_map(user.household_id)
        usages, missing_count = self._calculate_missing(recipe, inventory_map)
        return RecipeDetail(
            recipe_id=recipe.id,
            recipe_name=recipe.name,
            description=recipe.description,
            cook_time_minutes=recipe.cook_time_minutes,
            difficulty=recipe.difficulty,
            servings=recipe.servings,
            steps=recipe.steps,
            ingredients=usages,
            nutrition_tip="适合工作日晚餐" if "worker_evening" in recipe.tags else "适合家庭日常做饭",
            can_cook_now=missing_count == 0,
        )

    def analyze_missing(self, user: User, payload: MissingAnalysisRequest) -> MissingAnalysisData:
        recipes = self.recipe_repo.list_by_ids(payload.recipe_ids)
        inventory_map = self._inventory_map(user.household_id)
        aggregated: dict[str, MissingIngredient] = {}
        recipe_results: list[MissingAnalysisRecipe] = []
        for recipe in recipes:
            usages, _ = self._calculate_missing(recipe, inventory_map, payload.servings)
            missing_ingredients = [
                MissingIngredient(
                    ingredient_base_id=usage.ingredient_base_id,
                    ingredient_name=usage.ingredient_name,
                    missing_quantity=usage.missing_quantity,
                    unit=usage.unit,
                )
                for usage in usages
                if usage.missing_quantity > 0
            ]
            for missing in missing_ingredients:
                key = missing.ingredient_base_id or missing.ingredient_name
                if key in aggregated:
                    aggregated[key].missing_quantity = round(aggregated[key].missing_quantity + missing.missing_quantity, 2)
                else:
                    aggregated[key] = missing.model_copy()
            recipe_results.append(
                MissingAnalysisRecipe(
                    recipe_id=recipe.id,
                    recipe_name=recipe.name,
                    missing_ingredients=missing_ingredients,
                )
            )
        return MissingAnalysisData(recipes=recipe_results, aggregated_missing=list(aggregated.values()))

    def get_takeout_alternatives(self, recipe_ids: list[str]) -> list[dict]:
        alternatives: list[dict] = []
        for recipe_id in recipe_ids:
            alternatives.extend(TAKEOUT_ALTERNATIVES.get(recipe_id, []))
        return alternatives[:3]
