from pydantic import BaseModel, ConfigDict, field_validator


class ItemRow(BaseModel):
    model_config = ConfigDict(extra='forbid', from_attributes=True)

    item_number: int
    name: str
    category: str
    is_bio: bool
    purchase_price: float
    suggested_retail_price: float

    @field_validator('name')
    @classmethod
    def normalize_name(cls, name: str) -> str:
        return name.strip()

    @field_validator('category')
    @classmethod
    def normalize_category(cls, category: str) -> str:
        return category.strip().lower()
