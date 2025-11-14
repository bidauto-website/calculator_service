from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.database.crud.base import BaseService

from app.database.models.destination import Destination
from app.database.schemas.destination import DestinationCreate, DestinationUpdate


class DestinationService(BaseService[Destination, DestinationCreate, DestinationUpdate]):
    DEFAULT_DESTINATION_NAME = "Klaipeda"
    def __init__(self, session: AsyncSession):
        super().__init__(Destination, session)

    async def get_by_name(self, name: str) -> Destination | None:
        result = await self.session.execute(
            select(Destination)
            .where(
                Destination.name.ilike(name),
            )
        )
        return result.scalar_one_or_none()

    async def get_default(self) -> Destination:
        result = await self.session.execute(
            select(Destination).where(Destination.is_default.is_(True))
        )
        response = result.scalar_one_or_none()

        if response:
            return response
        result = await self.session.execute(
            select(Destination).where(Destination.name == self.DEFAULT_DESTINATION_NAME)
        )
        response = result.scalars().first()
        if not response:
            response = Destination(
                name=self.DEFAULT_DESTINATION_NAME,
                is_default=True
            )
            self.session.add(response)
        else:
            response.is_default = True
            self.session.add(response)
        try:
            await self.session.commit()
            await self.session.refresh(response)
            return response
        except Exception as e:
            logger.error('Error setting default destination', exc_info=e)
            await self.session.rollback()
            raise e






