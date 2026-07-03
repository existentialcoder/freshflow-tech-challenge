from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..api.deps.db import Base

if TYPE_CHECKING:
    from .item import Item


class OrderableItem(Base):
    __tablename__ = 'orderable_items'

    store_id: Mapped[str] = mapped_column(primary_key=True)
    item_number: Mapped[int] = mapped_column(ForeignKey('items.item_number'), primary_key=True)
    ordering_day: Mapped[date] = mapped_column(primary_key=True)
    delivery_day: Mapped[date]
    purchase_price: Mapped[float | None]
    suggested_retail_price: Mapped[float]
    profit_margin: Mapped[float | None]
    tags: Mapped[str | None]

    item: Mapped['Item'] = relationship()
