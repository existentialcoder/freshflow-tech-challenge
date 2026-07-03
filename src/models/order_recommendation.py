from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..api.deps.db import Base

if TYPE_CHECKING:
    from .item import Item


class OrderRecommendation(Base):
    __tablename__ = 'order_recommendations'
    __table_args__ = (
        Index('idx_store_orderday_recommendations', 'store_id', 'ordering_day'),
    )

    store_id: Mapped[str] = mapped_column(primary_key=True)
    item_number: Mapped[int] = mapped_column(ForeignKey('items.item_number'), primary_key=True)
    ordering_day: Mapped[date] = mapped_column(primary_key=True)
    delivery_day: Mapped[date]
    recommended_quantity: Mapped[float]

    item: Mapped['Item'] = relationship(lazy='joined')
