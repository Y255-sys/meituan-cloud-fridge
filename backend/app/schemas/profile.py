from app.schemas.common import AppBaseModel


class UserProfile(AppBaseModel):
    user_id: str
    nickname: str
    phone: str
    household_name: str
    senior_mode_enabled: bool
    dietary_preferences: list[str]
    allergy_tags: list[str]
    taste_tags: list[str]
    city_code: str


class UpdateProfileRequest(AppBaseModel):
    nickname: str | None = None
    dietary_preferences: list[str] | None = None
    allergy_tags: list[str] | None = None
    taste_tags: list[str] | None = None
    city_code: str | None = None

