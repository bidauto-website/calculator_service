from typing import Any, Coroutine, Sequence

from sqlalchemy import select, and_, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models import DeliveryPrice, Terminal, Location, VehicleType
from app.database.schemas.delivery_price import DeliveryPriceUpdate, DeliveryPriceCreate


class DeliveryPriceService(BaseService[DeliveryPrice, DeliveryPriceCreate, DeliveryPriceUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(DeliveryPrice, session)

    async def create_with_terminal_location_vehicle_type(self, price: int, terminal: Terminal, location: Location, vehicle_type: VehicleType):
        delivery_price = DeliveryPrice(price=price, terminal=terminal, location=location, vehicle_type=vehicle_type)
        self.session.add(delivery_price)
        await self.session.commit()
        await self.session.refresh(delivery_price)
        return delivery_price

    async def get_by_terminal_location_vehicle_type(
        self,
        location: Location,
        vehicle_type: VehicleType,
        terminal: Terminal = None,
    ) -> Sequence[DeliveryPrice]:
        conditions = [DeliveryPrice.location_id == location.id, DeliveryPrice.vehicle_type_id == vehicle_type.id]
        if terminal:
            conditions.append(DeliveryPrice.terminal_id == terminal.id)

        result = await self.session.execute(
            select(DeliveryPrice).where(
                and_(
                    *conditions
                )
            )
        )
        return result.scalars().all()


