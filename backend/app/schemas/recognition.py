from app.schemas.common import AppBaseModel


class RecognitionItem(AppBaseModel):
    temp_id: str
    ingredient_base_id: str | None
    ingredient_name: str
    quantity: float
    unit: str
    confidence: float
    source: str
    editable: bool
    suggested_storage_location: str
    suggested_expire_days: int


class RecognitionResult(AppBaseModel):
    recognition_id: str
    image_url: str
    items: list[RecognitionItem]

