from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .item import ItemRow

class OrderRecommendationRow(BaseModel):
    model_config = ConfigDict(extra='forbid', from_attributes=True)

    store_id: str
    item_number: int
    ordering_day: date
    delivery_day: date
    recommended_quantity: float

    @field_validator('store_id')
    @classmethod
    def normalize_store_id(cls, store_id: str) -> str:
        return store_id.strip().lower()

class IndividualRecommendation(OrderRecommendationRow):
    item_number: int = Field(exclude=True)
    store_id: str = Field(exclude=True)
    ordering_day: date = Field(exclude=True)
    item: ItemRow

    
class RecommendationRequestParams(BaseModel):

    store_id: str
    ordering_day: date

class RecommendationsMeta(BaseModel):
    model_config = ConfigDict(extra='forbid')

    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

class RecommendationsResult(BaseModel):
    model_config = ConfigDict(extra='forbid')

    store_id: str
    ordering_day: date
    recommendations: list[IndividualRecommendation]

class RecommendationsResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')

    result: RecommendationsResult
    meta: RecommendationsMeta
