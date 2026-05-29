from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.profile import UpdateProfileRequest, UserProfile


class ProfileService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repo = UserRepository(db)

    def get_profile(self, user: User) -> UserProfile:
        household_name = user.household.name if user.household else "我的家庭"
        return UserProfile(
            user_id=user.id,
            nickname=user.nickname,
            phone=user.phone,
            household_name=household_name,
            senior_mode_enabled=user.senior_mode_enabled,
            dietary_preferences=user.dietary_preferences,
            allergy_tags=user.allergy_tags,
            taste_tags=user.taste_tags,
            city_code=user.city_code,
        )

    def update_profile(self, user: User, payload: UpdateProfileRequest) -> UserProfile:
        for field_name, value in payload.model_dump(exclude_none=True).items():
            setattr(user, field_name, value)
        self.user_repo.update(user)
        return self.get_profile(user)

    def toggle_senior_mode(self, user: User, enabled: bool) -> dict[str, bool]:
        user.senior_mode_enabled = enabled
        self.user_repo.update(user)
        return {"enabled": enabled}

