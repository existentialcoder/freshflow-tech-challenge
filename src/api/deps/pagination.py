from fastapi import Query, HTTPException
from math import ceil
from typing import Generic, List, Optional, TypeVar, Dict

from pydantic import BaseModel
from ...core.constants import Constants

T = TypeVar('T', bound=BaseModel)


class PaginatedResponse(BaseModel, Generic[T]):
    meta: Dict[str, int]
    results: List[T]


def pagination_params(
    page: Optional[int] = Query(1, ge=1, description='Page number'),
    per_page: Optional[int] = Query(
        Constants.DEFAULT_PAGE_SIZE, ge=1, le=Constants.MAX_PAGE_SIZE, description='Items per page'
    ),
):
    return {'page': page, 'per_page': per_page}


def paginate_query(query, pagination: dict):
    page = pagination.get('page', 1)
    per_page = pagination.get('per_page', Constants.DEFAULT_PAGE_SIZE)

    if per_page > Constants.MAX_PAGE_SIZE:
        raise HTTPException(status_code=400, detail=f'per_page cannot exceed {Constants.MAX_PAGE_SIZE}')

    offset = (page - 1) * per_page
    return query.limit(per_page).offset(offset)


def build_paginated_response(items: list, key: str, total: int, page: int, per_page: int):
    total_pages = ceil(total / per_page) if total > 0 else 1

    result = {
        'meta': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1,
        }
    }

    result[key] = items

    return result
