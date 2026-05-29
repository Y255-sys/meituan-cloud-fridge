from pydantic import Field

from app.schemas.common import AppBaseModel


class UserSummary(AppBaseModel):
    id: str
    phone: str
    nickname: str


class RegisterRequest(AppBaseModel):
    phone: str = Field(min_length=11, max_length=20)
    password: str = Field(min_length=8, max_length=64)
    nickname: str = Field(min_length=1, max_length=50)


class LoginRequest(AppBaseModel):
    phone: str = Field(min_length=11, max_length=20)
    password: str = Field(min_length=8, max_length=64)


class AuthPayload(AppBaseModel):
    user: UserSummary
    token: str
