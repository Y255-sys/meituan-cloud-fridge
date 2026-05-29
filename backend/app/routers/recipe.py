from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import ApiResponse, build_success
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.recipe import MissingAnalysisData, MissingAnalysisRequest, RecipeDetail, RecipeRecommendationsData
from app.services.recipe import RecipeService

router = APIRouter(tags=["recipe"])


@router.get("/recipes/recommendations", response_model=ApiResponse[RecipeRecommendationsData])
def get_recommendations(
    meal_type: str = "dinner",
    servings: int = 2,
    scene: str = "worker_evening",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[RecipeRecommendationsData]:
    data = RecipeService(db).get_recommendations(current_user, meal_type, servings, scene)
    return build_success(data)


@router.get("/recipes/{recipe_id}", response_model=ApiResponse[RecipeDetail])
def get_recipe_detail(
    recipe_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[RecipeDetail]:
    data = RecipeService(db).get_recipe_detail(current_user, recipe_id)
    return build_success(data)


@router.post("/recipes/missing-analysis", response_model=ApiResponse[MissingAnalysisData])
def analyze_missing(
    payload: MissingAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiResponse[MissingAnalysisData]:
    data = RecipeService(db).analyze_missing(current_user, payload)
    return build_success(data)

