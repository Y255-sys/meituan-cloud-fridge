from app.schemas.common import AppBaseModel


class OrderSyncRequest(AppBaseModel):
    channel: str
    external_order_id: str


class OrderSyncData(AppBaseModel):
    synced: bool
    order_id: str
    imported_items: int

