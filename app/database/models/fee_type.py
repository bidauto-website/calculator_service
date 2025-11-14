from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models import Base, Fee
from app.enums.auction import AuctionEnum
from app.enums.fee_type import FeeTypeEnum


class FeeType(Base):
    __tablename__ = "fee_type"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    auction: Mapped[AuctionEnum] = mapped_column(SQLAlchemyEnum(AuctionEnum), nullable=False)
    fee_type: Mapped[FeeTypeEnum] = mapped_column(SQLAlchemyEnum(FeeTypeEnum),
                                                  default=FeeTypeEnum.NON_CLEAN_TITLE_FEE, nullable=False)

    fees: Mapped[list[Fee]] = relationship(
        'Fee',
        back_populates='fee_type',
        lazy='selectin'

    )







