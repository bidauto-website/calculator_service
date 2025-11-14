from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models import Base
from app.enums.auction import AuctionEnum, SpecificAuctionEnum
from app.enums.vehicle_type import VehicleTypeEnum

if TYPE_CHECKING:
    from app.database.models.location import Location
    from app.database.models.terminal import Terminal
    from app.database.models.shipping_price import ShippingPrice
    from app.database.models.delivery_price import DeliveryPrice


class VehicleType(Base):
    __tablename__ = "vehicle_type"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    auction: Mapped[AuctionEnum | None] = mapped_column(SQLAlchemyEnum(AuctionEnum), nullable=True)
    vehicle_type: Mapped[VehicleTypeEnum | None] = mapped_column(SQLAlchemyEnum(VehicleTypeEnum), nullable=True)

    specific_type: Mapped[SpecificAuctionEnum | None] = mapped_column(SQLAlchemyEnum(SpecificAuctionEnum),
                                                               nullable=True, default=None)

    shipping_prices: Mapped[list["ShippingPrice"]] = relationship(
        back_populates="vehicle_type",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    delivery_prices: Mapped[list["DeliveryPrice"]] = relationship(
        back_populates="vehicle_type",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
