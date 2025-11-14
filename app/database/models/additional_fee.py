from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models import Base


class AdditionalFee(Base):
    __tablename__ = "additional_fee"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    int_proxy_min: Mapped[float] = mapped_column(nullable=True, default=None)
    int_proxy_max: Mapped[float] = mapped_column(nullable=True, default=None)
    int_fee: Mapped[float] = mapped_column(nullable=True, default=None)
    proxy_fee: Mapped[float] = mapped_column(nullable=True, default=None)

    live_bid_min: Mapped[float] = mapped_column(nullable=True, default=None)
    live_bid_max: Mapped[float] = mapped_column(nullable=True, default=None)
    live_bid_fee: Mapped[float] = mapped_column(nullable=True, default=None)

    __table_args__ = (
        Index('idx_int_proxy_range', 'int_proxy_min', 'int_proxy_max'),
        Index('idx_live_bid_range', 'live_bid_min', 'live_bid_max'),
    )





