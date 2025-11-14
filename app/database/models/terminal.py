from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.models import Base

if TYPE_CHECKING:
    from app.database.models.delivery_price import DeliveryPrice
    from app.database.models.vehicle_type import VehicleType
    from app.database.models.shipping_price import ShippingPrice

class Terminal(Base):
    __tablename__ = "terminal"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    delivery_prices: Mapped[list["DeliveryPrice"]] = relationship(
        "DeliveryPrice",
        back_populates="terminal",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    shipping_prices: Mapped[list["ShippingPrice"]] = relationship(
        "ShippingPrice",
        back_populates="terminal",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


