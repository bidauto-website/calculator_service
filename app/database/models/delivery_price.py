from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database.models import Base

if TYPE_CHECKING:
    from app.database.models.location import Location
    from app.database.models.terminal import Terminal
    from app.database.models.vehicle_type import VehicleType

class DeliveryPrice(Base):
    __tablename__ = "delivery_price"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    location_id: Mapped[int] = mapped_column(
        ForeignKey("location.id"),
        nullable=False,
        index=True
    )
    terminal_id: Mapped[int] = mapped_column(
        ForeignKey("terminal.id"),
        nullable=False,
        index=True
    )

    vehicle_type_id: Mapped[int] = mapped_column(ForeignKey("vehicle_type.id"), nullable=False, index=True)


    price: Mapped[int] = mapped_column(nullable=False)

    location: Mapped["Location"] = relationship(back_populates="delivery_prices",
        lazy="selectin")
    terminal: Mapped["Terminal"] = relationship(
        "Terminal",
        back_populates="delivery_prices",
        lazy="selectin",
    )
    vehicle_type: Mapped["VehicleType"] = relationship(
        back_populates="delivery_prices",
        lazy="selectin"
    )