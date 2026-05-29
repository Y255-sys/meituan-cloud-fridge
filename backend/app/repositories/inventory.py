from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.ingredient import UserIngredient


class InventoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _base_query(self, household_id: str) -> Select[tuple[UserIngredient]]:
        return select(UserIngredient).where(UserIngredient.household_id == household_id)

    def list_items(
        self,
        household_id: str,
        keyword: str | None = None,
        category: str | None = None,
        status: str | None = None,
        storage_location: str | None = None,
        sort_by: str | None = None,
    ) -> list[UserIngredient]:
        query = self._base_query(household_id)
        if keyword:
            like_pattern = f"%{keyword}%"
            query = query.where(UserIngredient.ingredient_name.ilike(like_pattern))
        if category:
            query = query.where(UserIngredient.category == category)
        if status:
            query = query.where(UserIngredient.status == status)
        if storage_location:
            query = query.where(UserIngredient.storage_location == storage_location)

        if sort_by == "updated_at":
            query = query.order_by(UserIngredient.updated_at.desc())
        else:
            query = query.order_by(UserIngredient.expire_at.asc().nullslast(), UserIngredient.updated_at.desc())

        return list(self.db.scalars(query).all())

    def count_by_status(self, household_id: str, status: str) -> int:
        query = select(func.count(UserIngredient.id)).where(
            UserIngredient.household_id == household_id,
            UserIngredient.status == status,
        )
        return int(self.db.scalar(query) or 0)

    def get_by_id(self, item_id: str) -> UserIngredient | None:
        return self.db.get(UserIngredient, item_id)

    def create(self, item: UserIngredient) -> UserIngredient:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def bulk_create(self, items: list[UserIngredient]) -> list[UserIngredient]:
        self.db.add_all(items)
        self.db.commit()
        for item in items:
            self.db.refresh(item)
        return items

    def update(self, item: UserIngredient) -> UserIngredient:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: UserIngredient) -> None:
        self.db.delete(item)
        self.db.commit()

