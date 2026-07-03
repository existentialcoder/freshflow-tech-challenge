import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..api.deps.pagination import build_paginated_response, paginate_query

from ..schemas.order_recommendation import IndividualRecommendation, RecommendationRequestParams

from ..models.order_recommendation import OrderRecommendation

logger = logging.getLogger(__name__)

async def list_all_recommendations(
    db: AsyncSession, recommendations_params: RecommendationRequestParams, pagination: dict
) -> dict:
    filters = (
        OrderRecommendation.store_id == recommendations_params.store_id,
        OrderRecommendation.ordering_day == recommendations_params.ordering_day,
        # make sure negative quantity is filtered
        OrderRecommendation.recommended_quantity >= 0
    )

    total = (
        await db.execute(select(func.count()).select_from(OrderRecommendation).where(*filters))
    ).scalar_one()

    q_stmt = paginate_query(select(OrderRecommendation).where(*filters), pagination)
    result = await db.execute(q_stmt)

    items = [IndividualRecommendation.model_validate(row) for row in result.scalars().all()]

    paginated = build_paginated_response(items, 'recommendations', total, pagination['page'], pagination['per_page'])

    return {
        'result': {
            'store_id': recommendations_params.store_id,
            'ordering_day': recommendations_params.ordering_day,
            'recommendations': paginated['recommendations'],
        },
        'meta': paginated['meta'],
    }
