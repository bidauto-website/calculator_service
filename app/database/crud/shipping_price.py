from typing import Any, Coroutine, Sequence

from sqlalchemy import select, or_, and_, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models import Location, VehicleType, ShippingPrice, Destination, Terminal

from app.database.schemas.shipping_price import ShippingPriceCreate, ShippingPriceUpdate


class ShippingPriceService(BaseService[ShippingPrice, ShippingPriceCreate, ShippingPriceUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(ShippingPrice, session)

    async def get_by_terminal_and_vehicle_type(self, terminal: Terminal, vehicle_type: VehicleType) -> \
    Sequence[ShippingPrice]:
        result = await self.session.execute(
            select(ShippingPrice)
            .where(
                and_(
                    ShippingPrice.terminal_id == terminal.id,
                    ShippingPrice.vehicle_type_id == vehicle_type.id
                )
            )
        )
        return result.scalars().all()

    async def get_by_destination_and_vehicle_type(self, destination: Destination, vehicle_type: VehicleType) -> \
    Sequence[ShippingPrice]:
        result = await self.session.execute(
            select(ShippingPrice)
            .where(
                and_(
                    ShippingPrice.destination_id == destination.id,
                    ShippingPrice.vehicle_type_id == vehicle_type.id
                )
            )
        )
        return result.scalars().all()

    async def create_by_destination_vehicle_type_terminal(self, price: int, destination: Destination,
                                                          vehicle_type: VehicleType, terminal: Terminal) -> ShippingPrice:
        obj = ShippingPrice(price=price, destination=destination, terminal=terminal, vehicle_type=vehicle_type)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_destination_vehicle_type_terminal_single(
        self,
        destination: Destination,
        vehicle_type: VehicleType,
        terminal: Terminal
    ) -> ShippingPrice | None:
        result = await self.session.execute(
            select(ShippingPrice).where(
                and_(
                    ShippingPrice.destination_id == destination.id,
                    ShippingPrice.vehicle_type_id == vehicle_type.id,
                    ShippingPrice.terminal_id == terminal.id,
                )
            )
        )
        return result.scalar_one_or_none()






