import csv
import io
import logging
import asyncio

from fastapi import UploadFile
from pydantic import BaseModel, ValidationError
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.data_loader import LoadDataRequest, LoadDataResponse, MetricsResponse
from ..schemas.inventory import InventoryRow
from ..schemas.item import ItemRow
from ..schemas.orderable_item import OrderableItemRow
from ..schemas.order_recommendation import OrderRecommendationRow

from ..models.item import Item
from ..models.inventory import Inventory
from ..models.orderable_item import OrderableItem
from ..models.order_recommendation import OrderRecommendation

logger = logging.getLogger(__name__)

ROW_SCHEMA_MAP: dict[str, type[BaseModel]] = {
    'items': ItemRow,
    'inventory': InventoryRow,
    'orderable_items': OrderableItemRow,
    'order_recommendations': OrderRecommendationRow,
}


async def _read_csv_file(file: UploadFile, row_model: type[BaseModel]) -> tuple[list[BaseModel], int]:
    content = await file.read()

    text = content.decode('utf-8-sig')
    rows = []
    skipped = 0

    for line_number, raw_row in enumerate(csv.DictReader(io.StringIO(text)), start=2):
        # Extra field values are dropped
        raw_row.pop(None, None)

        try:
            rows.append(row_model(**raw_row))
        # Incase of an unexpected row on CSV
        except ValidationError as ex:
            skipped += 1
            logger.warning(f'Row {line_number} skipped. Exception: {ex}')

    return rows, skipped


async def _read_csv_files(load_data_request: LoadDataRequest) -> dict[str, tuple[list[BaseModel], int]]:
    results = await asyncio.gather(
        *(
            _read_csv_file(getattr(load_data_request, field_name), row_schema)
            for field_name, row_schema in ROW_SCHEMA_MAP.items()
        )
    )

    return dict(zip(ROW_SCHEMA_MAP.keys(), results))

async def _ingest_items(db: AsyncSession, items: list[ItemRow]) -> tuple[set[int], int, int]:
    # Existing item numbers
    valid_item_numbers = set((await db.execute(select(Item.item_number))).scalars().all())
    items_to_insert = []
    skipped = 0

    for row in items:
        if row.item_number in valid_item_numbers:
            skipped += 1
            logger.warning(f'Item skipped as its a duplicate. item_number : {row.item_number}')
            continue

        valid_item_numbers.add(row.item_number)
        items_to_insert.append(row.model_dump())

    if items_to_insert and len(items_to_insert) > 0:
        await db.execute(insert(Item), items_to_insert)

    return valid_item_numbers, len(items_to_insert), skipped

"""
Takes a list of rows and ingests them into the database.
It checks for duplicates based on the key_columns and skips any rows that are duplicates or have invalid item_numbers.
It returns the number of rows inserted and the number of rows skipped.
"""
async def _ingest_rows(
    db: AsyncSession,
    rows: list[BaseModel],
    model: type,
    key_columns: tuple[str, str, str],
    valid_item_numbers: set[int],
    exclude_fields: set[str] | None = None,
) -> tuple[int, int]:
    existing_keys = {
        tuple(row) for row in (await db.execute(select(*(getattr(model, col) for col in key_columns)))).all()
    }
    seen_keys: set[tuple] = set()
    to_insert = []
    skipped = 0

    for row in rows:
        if row.item_number not in valid_item_numbers:
            skipped += 1
            logger.warning(f'{model.__name__} skipped as item_number {row.item_number} does not exist.')
            continue

        key = tuple(getattr(row, column) for column in key_columns)
        if key in existing_keys or key in seen_keys:
            skipped += 1
            logger.warning(f'{model.__name__} skipped as its a duplicate. {dict(zip(key_columns, key))}')
            continue

        seen_keys.add(key)
        to_insert.append(row.model_dump(exclude=exclude_fields or set()))

    if to_insert and len(to_insert) > 0:
        await db.execute(insert(model), to_insert)

    return len(to_insert), skipped


async def load_data(db: AsyncSession, load_data_request: LoadDataRequest) -> LoadDataResponse:
    logger.info('Loading data...')
    parsed_files = await _read_csv_files(load_data_request)

    items, items_skipped = parsed_files['items']
    inventory, inventory_skipped = parsed_files['inventory']
    orderable_items, orderable_items_skipped = parsed_files['orderable_items']
    order_recommendations, order_recommendations_skipped = parsed_files['order_recommendations']

    async with db.begin():
        valid_item_numbers, items_loaded, items_ingest_skipped = await _ingest_items(db, items)

        inventory_loaded, inventory_ingest_skipped = await _ingest_rows(
            db, inventory, Inventory, ('store_id', 'item_number', 'day'), valid_item_numbers,
        )
        orderable_items_loaded, orderable_items_ingest_skipped = await _ingest_rows(
            db, orderable_items, OrderableItem, ('store_id', 'item_number', 'ordering_day'), valid_item_numbers,
            exclude_fields={'category'},
        )
        order_recommendations_loaded, order_recommendations_ingest_skipped = await _ingest_rows(
            db, order_recommendations, OrderRecommendation, ('store_id', 'item_number', 'ordering_day'),
            valid_item_numbers,
        )

    return LoadDataResponse(
        items=MetricsResponse(loaded=items_loaded, skipped=items_skipped + items_ingest_skipped),
        inventory=MetricsResponse(loaded=inventory_loaded, skipped=inventory_skipped + inventory_ingest_skipped),
        orderable_items=MetricsResponse(
            loaded=orderable_items_loaded, skipped=orderable_items_skipped + orderable_items_ingest_skipped
        ),
        order_recommendations=MetricsResponse(
            loaded=order_recommendations_loaded,
            skipped=order_recommendations_skipped + order_recommendations_ingest_skipped,
        )
    )
