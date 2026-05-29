from enum import StrEnum


class StorageLocation(StrEnum):
    CHILLED = "冷藏"
    FROZEN = "冷冻"
    AMBIENT = "常温"


class InventoryStatus(StrEnum):
    FRESH = "fresh"
    EXPIRING = "expiring"
    EXPIRED = "expired"


class InventorySourceType(StrEnum):
    MANUAL = "manual"
    RECOGNITION = "recognition"
    ORDER_SYNC = "order_sync"


class RecommendationGroupType(StrEnum):
    COOK_NOW = "cook_now"
    BUY_LITTLE = "buy_little"
    TAKEOUT = "takeout"


class PurchaseStrategy(StrEnum):
    LOWEST_COST = "lowest_cost"
    MINIMUM_ITEMS = "minimum_items"

