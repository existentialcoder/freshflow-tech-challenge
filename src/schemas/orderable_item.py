from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class OrderableItemRow(BaseModel):
    model_config = ConfigDict(extra='forbid')

    store_id: str
    item_number: int
    ordering_day: date
    delivery_day: date
    purchase_price: float | None
    suggested_retail_price: float
    profit_margin: float | None
    tags: str | None
    category: str

    @field_validator('store_id')
    @classmethod
    def normalize_store_id(cls, store_id: str) -> str:
        return store_id.strip().lower()

    @field_validator('purchase_price', 'profit_margin', mode='before')
    @classmethod
    def blank_to_none(cls, value: Any) -> Any:
        if isinstance(value, str) and value.strip() == '':
            return None
        return value

    @field_validator('tags')
    @classmethod
    def normalize_tags(cls, tags: str | None) -> str | None:
        if tags is None:
            return None
        return tags.strip().lower() or None

    @field_validator('category')
    @classmethod
    def normalize_category(cls, category: str) -> str:
        return category.strip().lower()
