from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ingredient import IngredientBase


class IngredientRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, ingredient_id: str) -> IngredientBase | None:
        return self.db.get(IngredientBase, ingredient_id)

    def get_by_name(self, ingredient_name: str) -> IngredientBase | None:
        return self.db.scalar(select(IngredientBase).where(IngredientBase.name == ingredient_name))

    def list_all(self) -> list[IngredientBase]:
        return list(self.db.scalars(select(IngredientBase)).all())

