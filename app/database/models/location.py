from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models import Base

if TYPE_CHECKING:
    from app.database.models.delivery_price import DeliveryPrice
    from app.database.models.vehicle_type import VehicleType
    from app.database.models.shipping_price import ShippingPrice


class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    city: Mapped[str] = mapped_column(nullable=True)
    state: Mapped[str] = mapped_column(nullable=True)
    postal_code: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)


    delivery_prices: Mapped[list["DeliveryPrice"]] = relationship(
        back_populates="location",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


