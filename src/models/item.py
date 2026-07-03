from sqlalchemy.orm import Mapped, mapped_column

from ..api.deps.db import Base


class Item(Base):
    __tablename__ = 'items'

    item_number: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category: Mapped[str]
    is_bio: Mapped[bool]
    purchase_price: Mapped[float]
    suggested_retail_price: Mapped[float]
