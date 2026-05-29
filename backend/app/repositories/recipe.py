from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.recipe import RecipeBase


class RecipeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[RecipeBase]:
        query = select(RecipeBase).options(selectinload(RecipeBase.ingredients)).order_by(RecipeBase.name.asc())
        return list(self.db.scalars(query).all())

    def get_by_id(self, recipe_id: str) -> RecipeBase | None:
        query = select(RecipeBase).options(selectinload(RecipeBase.ingredients)).where(RecipeBase.id == recipe_id)
        return self.db.scalar(query)

    def list_by_ids(self, recipe_ids: list[str]) -> list[RecipeBase]:
        query = select(RecipeBase).options(selectinload(RecipeBase.ingredients)).where(RecipeBase.id.in_(recipe_ids))
        return list(self.db.scalars(query).all())

