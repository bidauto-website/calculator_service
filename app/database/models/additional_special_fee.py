from sqlalchemy.orm import Mapped, mapped_column
from app.database.models import Base
from app.enums.auction import AuctionEnum


class AdditionalSpecialFee(Base):
    __tablename__ = "additional_special_fee"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(nullable=False)
    auction: Mapped[AuctionEnum] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)






