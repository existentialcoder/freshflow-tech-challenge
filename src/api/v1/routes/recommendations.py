from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.deps.db import get_db
from ....api.deps.pagination import pagination_params
from ....schemas.order_recommendation import RecommendationRequestParams, RecommendationsResponse
from ....services import recommendations as recommendations_service

router = APIRouter(prefix='/recommendations')

@router.get(
    '',
    response_model=RecommendationsResponse,
    description='List all recommendations',
)
async def list_recommendations(
    recommendations_params: Annotated[RecommendationRequestParams, Query()],
    pagination: dict = Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
):
   return await recommendations_service.list_all_recommendations(db, recommendations_params, pagination)
