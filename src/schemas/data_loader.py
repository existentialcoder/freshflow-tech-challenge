from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, field_validator


class LoadDataRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    items: UploadFile
    orderable_items: UploadFile
    inventory: UploadFile
    order_recommendations: UploadFile

    @field_validator('items', 'orderable_items', 'inventory', 'order_recommendations')
    @classmethod
    def validate_if_csv(cls, file: UploadFile) -> UploadFile:
        if not file.filename or not file.filename.lower().endswith('.csv'):
            raise ValueError(f'"{file.filename or ""}" must be a .csv file')
        return file


class MetricsResponse(BaseModel):
    loaded: int
    skipped: int

class LoadDataResponse(BaseModel):
    items: MetricsResponse
    inventory: MetricsResponse
    orderable_items: MetricsResponse
    order_recommendations: MetricsResponse
