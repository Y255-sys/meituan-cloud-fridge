from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.base import generate_prefixed_id
from app.models.household import Household
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import AuthPayload, LoginRequest, RegisterRequest, UserSummary


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, payload: RegisterRequest) -> AuthPayload:
        if self.user_repo.get_by_phone(payload.phone):
            raise AppException(code=40900, message="phone already registered", status_code=409)

        household = Household(id=generate_prefixed_id("house"), name=f"{payload.nickname}家", owner_user_id=None)
        self.db.add(household)
        self.db.flush()

        user = User(
            id=generate_prefixed_id("usr"),
            phone=payload.phone,
            password_hash=hash_password(payload.password),
            nickname=payload.nickname,
            household_id=household.id,
            senior_mode_enabled=False,
            city_code="310100",
            dietary_preferences=[],
            allergy_tags=[],
            taste_tags=[],
        )
        self.db.add(user)
        self.db.flush()
        household.owner_user_id = user.id
        self.db.commit()
        self.db.refresh(user)

        token = create_access_token(user.id)
        return AuthPayload(user=UserSummary.model_validate(user), token=token)

    def login(self, payload: LoginRequest) -> AuthPayload:
        user = self.user_repo.get_by_phone(payload.phone)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise AppException(code=40100, message="invalid phone or password", status_code=401)

        token = create_access_token(user.id)
        return AuthPayload(user=UserSummary.model_validate(user), token=token)

