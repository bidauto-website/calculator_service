from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService
from app.database.models import VehicleType
from app.database.models.terminal import Terminal

from app.database.schemas.terminal import TerminalCreate, TerminalUpdate


class TerminalService(BaseService[Terminal, TerminalCreate, TerminalUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Terminal, session)

    async def get_by_name(self, name: str)-> Terminal | None:
        result = await self.session.execute(
            select(Terminal).where(Terminal.name == name)
        )
        return result.scalar_one_or_none()

    








