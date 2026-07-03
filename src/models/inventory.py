from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..api.deps.db import Base

if TYPE_CHECKING:
    from .item import Item


class Inventory(Base):
    __tablename__ = 'inventory'

    store_id: Mapped[str] = mapped_column(primary_key=True)
    item_number: Mapped[int] = mapped_column(ForeignKey('items.item_number'), primary_key=True)
    day: Mapped[date] = mapped_column(primary_key=True)
    quantity: Mapped[float]

    item: Mapped['Item'] = relationship()
