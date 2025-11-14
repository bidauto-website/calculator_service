from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.models import Base

if TYPE_CHECKING:
    from app.database.models.location import Location
    from app.database.models.terminal import Terminal
    from app.database.models.destination import Destination
    from app.database.models.vehicle_type import VehicleType


class ShippingPrice(Base):
    __tablename__ = "shipping_price"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    terminal_id: Mapped[int] = mapped_column(
        ForeignKey("terminal.id"),
        nullable=False,
        index=True
    )
    destination_id: Mapped[int] = mapped_column(
        ForeignKey("destination.id"),
        nullable=False,
        index=True
    )
    vehicle_type_id: Mapped[int] = mapped_column(ForeignKey("vehicle_type.id"), nullable=False, index=True)


    price: Mapped[int] = mapped_column(nullable=False)


    destination: Mapped["Destination"] = relationship(
        back_populates="shipping_prices",
        lazy="selectin"
    )
    terminal: Mapped["Terminal"] = relationship(
        back_populates="shipping_prices",
        lazy="selectin"
    )
    vehicle_type: Mapped["VehicleType"] = relationship(
        back_populates="shipping_prices",
        lazy="selectin"
    )