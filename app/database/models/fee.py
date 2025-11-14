from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLAlchemyEnum, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models import Base

if TYPE_CHECKING:
    from app.database.models.fee_type import FeeType


class Fee(Base):
    __tablename__ = "fee"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    car_price_min: Mapped[float] = mapped_column(nullable=False)
    car_price_max: Mapped[float] = mapped_column(nullable=False)
    car_price_fee: Mapped[float] = mapped_column(nullable=False)

    fee_type_id: Mapped[int] = mapped_column(ForeignKey("fee_type.id"), nullable=False)

    __table_args__ = (
        Index('idx_fee_type_price_range', 'fee_type_id', 'car_price_min', 'car_price_max'),
    )

    fee_type: Mapped['FeeType'] = relationship(
        "FeeType",
        back_populates="fees",
        lazy="selectin",
    )







