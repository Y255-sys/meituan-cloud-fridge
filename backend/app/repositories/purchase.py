from sqlalchemy.orm import Session

from app.models.purchase_plan import PurchasePlan


class PurchasePlanRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, plan: PurchasePlan) -> PurchasePlan:
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def get_by_id(self, plan_id: str) -> PurchasePlan | None:
        return self.db.get(PurchasePlan, plan_id)

