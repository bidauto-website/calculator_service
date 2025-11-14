import re

from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.base import BaseService, CreateSchemaType, ModelType
from app.database.models import Location, VehicleType, ShippingPrice, DeliveryPrice

from app.database.schemas.location import LocationCreate, LocationUpdate
from app.enums.auction import AuctionEnum


class LocationService(BaseService[Location, LocationCreate, LocationUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Location, session)

    async def get_location(self, location_name: str,
                           vehicle_type: VehicleType,
                           city: str | None = None,
                           state: str | None = None) -> Location | None:

        clean_name = re.sub(r'\s*\([^)]*\)', '', location_name).strip()
        texted_location = f"{city} {state}" if city and state else ""

        async def search_by_conditions(conditions: list) -> Location | None:
            for condition in conditions:
                try:
                    result = await self.session.execute(
                        select(Location)
                        .join(DeliveryPrice)
                        .where(and_(condition, DeliveryPrice.vehicle_type_id == vehicle_type.id))
                        .distinct()
                        .limit(1)
                    )
                    location = result.scalar_one_or_none()
                    if location:
                        return location
                except Exception:
                    continue
            return None

        search_conditions = []

        if location_name:
            search_conditions.extend([
                Location.name.ilike(location_name),
                Location.name.ilike(clean_name),
            ])

        if city and state:
            search_conditions.extend([
                Location.name.ilike(f"{city} {state}"),
                and_(Location.city.ilike(city), Location.state.ilike(state)),
                and_(Location.name.ilike(f"%{city}%"), Location.state.ilike(state)),
            ])

        patterns = ['%{}%', '{}%', '%{}']
        fields_and_values = [
            (Location.name, clean_name),
            (Location.city, city),
            (Location.name, city),
            (Location.name, texted_location),
            (Location.city, texted_location),
        ]

        for field, value in fields_and_values:
            if value:
                search_conditions.extend([field.ilike(pattern.format(value)) for pattern in patterns])

        result = await search_by_conditions(search_conditions)
        if result:
            return result

        if city and ' ' in city:
            keywords = city.split()
            keyword_conditions = [
                or_(
                    Location.name.ilike(f"%{kw}%"),
                    Location.city.ilike(f"%{kw}%"),
                    Location.state.ilike(f"%{kw}%")
                ) for kw in keywords
            ]
            return await search_by_conditions([and_(*keyword_conditions)])

        return None

    async def get_location_fuzzy(self, location_name: str,
                                 vehicle_type: VehicleType,
                                 city: str | None = None,
                                 state: str | None = None,
                                 threshold: float = 0.6) -> Location | None:
        location = await self.get_location(location_name, vehicle_type, city, state)
        if location:
            return location

        for term in filter(None, [location_name, city, state]):
            try:
                result = await self.session.execute(
                    select(Location)
                    .join(DeliveryPrice)
                    .where(and_(
                        DeliveryPrice.vehicle_type_id == vehicle_type.id,
                        or_(
                            func.similarity(Location.name, term) > threshold,
                            func.similarity(Location.city, term) > threshold
                        )
                    ))
                    .order_by(desc(func.greatest(
                        func.similarity(Location.name, term),
                        func.similarity(Location.city, term)
                    )))
                    .limit(1)
                )

                location = result.scalar_one_or_none()
                if location:
                    return location
            except Exception:
                continue

        return None

    async def find_location(self, location_name: str,
                            vehicle_type: VehicleType,
                            city: str | None = None,
                            state: str | None = None) -> Location | None:

        search_methods = [
            self.get_location,
            self.get_location_fuzzy,
        ]

        for method in search_methods:
            try:
                location = await method(location_name, vehicle_type, city, state)
                if location:
                    return location
            except Exception:
                continue

        return None

    async def get_by_name(self, name: str) -> Location | None:
        result = await self.session.execute(
            select(Location).where(Location.name == name)
        )
        return result.scalar_one_or_none()

    async def get_with_search_auction(self,
                                      search: str | None = None,
                                      auction: AuctionEnum | None = None,
                                      get_stmt: bool = False):
        stmt = select(Location).distinct()

        filters = []

        if search:
            search_value = search.strip()
            if search_value:
                pattern = f"%{search_value}%"
                filters.append(or_(
                    Location.name.ilike(pattern),
                    Location.city.ilike(pattern),
                    Location.state.ilike(pattern)
                ))

        if auction:
            stmt = stmt.join(DeliveryPrice).join(VehicleType)
            filters.append(VehicleType.auction == auction)

        if filters:
            stmt = stmt.where(and_(*filters))

        if get_stmt:
            return stmt

        result = await self.session.execute(stmt)
        return result.scalars().unique().all()












