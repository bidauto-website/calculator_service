from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models import Base

if TYPE_CHECKING:
    from app.database.models.shipping_price import ShippingPrice

class Destination(Base):
    __tablename__ = "destination"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_default: Mapped[bool] = mapped_column(default=False)

    shipping_prices: Mapped[list["ShippingPrice"]] = relationship(
        "ShippingPrice",
        back_populates="destination",
        cascade="all, delete-orphan",
        lazy="selectin",
    )





