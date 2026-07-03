from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class InventoryRow(BaseModel):
    model_config = ConfigDict(extra='forbid')

    store_id: str
    item_number: int
    day: date
    quantity: float

    @field_validator('store_id')
    @classmethod
    def normalize_store_id(cls, store_id: str) -> str:
        return store_id.strip().lower()

    @field_validator('day', mode='before')
    @classmethod
    def parse_date(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%d/%m/%Y').date()
            except ValueError:
                pass
        return value
