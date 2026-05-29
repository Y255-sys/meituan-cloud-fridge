from typing import Generic, TypeVar
from uuid import uuid4

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: T | None
    request_id: str


def build_success(data: T, message: str = "ok") -> ApiResponse[T]:
    return ApiResponse(code=0, message=message, data=data, request_id=f"req_{uuid4().hex[:12]}")


def build_error(code: int, message: str) -> ApiResponse[None]:
    return ApiResponse(code=code, message=message, data=None, request_id=f"req_{uuid4().hex[:12]}")

