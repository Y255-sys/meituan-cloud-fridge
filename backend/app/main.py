from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import AppException
from app.core.response import build_error
from app.mock_data.demo_data import seed_demo_data
from app.routers import auth, inventory, order_sync, profile, purchase, recognition, recipe, senior_mode

# Import models so SQLAlchemy metadata is complete before create_all.
from app import models  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.auto_create_tables:
        Base.metadata.create_all(bind=engine)
    if settings.auto_seed_demo_data:
        seed_demo_data()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
    payload = build_error(exc.code, exc.message)
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
async def handle_validation_exception(_: Request, exc: RequestValidationError) -> JSONResponse:
    payload = build_error(40001, "data validation failed")
    content = payload.model_dump()
    content["data"] = {"errors": exc.errors()}
    return JSONResponse(status_code=422, content=content)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(profile.router, prefix=settings.api_prefix)
app.include_router(senior_mode.router, prefix=settings.api_prefix)
app.include_router(recognition.router, prefix=settings.api_prefix)
app.include_router(inventory.router, prefix=settings.api_prefix)
app.include_router(order_sync.router, prefix=settings.api_prefix)
app.include_router(recipe.router, prefix=settings.api_prefix)
app.include_router(purchase.router, prefix=settings.api_prefix)
