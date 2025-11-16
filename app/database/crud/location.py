import re
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.database.models import Location, DeliveryPrice, VehicleType


class LocationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _parse_location_input(self, location_name: str) -> tuple[str, str | None]:
        """Парсит входную строку и извлекает штат и название локации"""
        if not location_name:
            return "", None

        # Обработка формата "STATE - Location Name"
        state_prefix_match = re.match(r'^([A-Z]{2})\s*[-–]\s*(.+)$', location_name.strip())
        if state_prefix_match:
            extracted_state = state_prefix_match.group(1)
            extracted_name = state_prefix_match.group(2).strip()
            return extracted_name, extracted_state

        return location_name.strip(), None

    def _clean_location_name(self, name: str) -> str:
        """Очищает название локации от лишних элементов"""
        if not name:
            return ""

        # Удаляем содержимое в скобках
        clean_name = re.sub(r'\s*\([^)]*\)', '', name).strip()

        # Удаляем почтовые индексы в конце (5 цифр)
        clean_name = re.sub(r'\s+\d{5}$', '', clean_name).strip()

        # Удаляем лишние пробелы
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()

        return clean_name

    def _generate_search_variants(self, name: str) -> list[str]:
        """Генерирует различные варианты названия для поиска"""
        if not name:
            return []

        variants = [name]
        clean_name = self._clean_location_name(name)

        if clean_name != name:
            variants.append(clean_name)

        # Добавляем варианты с разными разделителями
        for separator in [' ', '-', '_']:
            if separator in clean_name:
                # Заменяем разделители на пробелы
                spaced_variant = re.sub(f'[{re.escape(separator)}]+', ' ', clean_name).strip()
                if spaced_variant not in variants:
                    variants.append(spaced_variant)

        return variants

    async def get_location(self, location_name: str,
                           vehicle_type: VehicleType,
                           city: str | None = None,
                           state: str | None = None) -> Location | None:

        # Парсим входные данные
        parsed_name, extracted_state = self._parse_location_input(location_name)

        # Используем извлеченный штат, если он не был передан отдельно
        if extracted_state and not state:
            state = extracted_state

        # Генерируем варианты названий для поиска
        name_variants = self._generate_search_variants(parsed_name)

        # Создаем текстовое представление локации
        location_text_parts = []
        if city:
            location_text_parts.append(city)
        if state:
            location_text_parts.append(state)
        location_text = " ".join(location_text_parts)

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

        # 1. Точные совпадения по названию (высший приоритет)
        for variant in name_variants:
            search_conditions.extend([
                Location.name.ilike(variant),
                func.upper(Location.name) == func.upper(variant),
            ])

        # 2. Поиск по городу и штату
        if city and state:
            search_conditions.extend([
                and_(Location.city.ilike(city), Location.state.ilike(state)),
                and_(func.upper(Location.city) == func.upper(city),
                     func.upper(Location.state) == func.upper(state)),
                Location.name.ilike(f"{city} {state}"),
                Location.name.ilike(f"{city}%{state}"),
            ])

        # 3. Поиск только по штату (для случаев когда город в названии)
        if state:
            search_conditions.extend([
                and_(Location.state.ilike(state),
                     or_(*[Location.name.ilike(f"%{variant}%") for variant in name_variants])),
                and_(func.upper(Location.state) == func.upper(state),
                     or_(*[func.upper(Location.name).like(f"%{func.upper(variant)}%") for variant in name_variants])),
            ])

        # 4. Паттерны поиска с wildcards
        patterns = ['%{}%', '{}%', '%{}']
        search_fields = [
            (Location.name, name_variants),
            (Location.city, [city] if city else []),
        ]

        if location_text:
            search_fields.append((Location.name, [location_text]))

        for field, values in search_fields:
            for value in values:
                if value:
                    search_conditions.extend([
                        field.ilike(pattern.format(value)) for pattern in patterns
                    ])

        # 5. Поиск с очищенными названиями из БД
        for variant in name_variants:
            search_conditions.extend([
                func.regexp_replace(Location.name, r'\s+\d{5}$', '', 'g').ilike(f"%{variant}%"),
                func.regexp_replace(func.upper(Location.name), r'\s+\d{5}$', '', 'g').like(f"%{variant.upper()}%"),
            ])

        # Выполняем поиск
        result = await search_by_conditions(search_conditions)
        if result:
            return result

        # 6. Поиск по ключевым словам (если в названии несколько слов)
        if parsed_name and ' ' in parsed_name:
            keywords = parsed_name.split()
            if len(keywords) >= 2:
                keyword_conditions = []

                # Все ключевые слова должны присутствовать
                all_keywords_condition = and_(
                    *[Location.name.ilike(f"%{kw}%") for kw in keywords]
                )
                keyword_conditions.append(all_keywords_condition)

                # Добавляем условие по штату если есть
                if state:
                    keyword_conditions.append(
                        and_(
                            Location.state.ilike(state),
                            all_keywords_condition
                        )
                    )

                result = await search_by_conditions(keyword_conditions)
                if result:
                    return result

        return None

    async def get_location_fuzzy(self, location_name: str,
                                 vehicle_type: VehicleType,
                                 city: str | None = None,
                                 state: str | None = None,
                                 threshold: float = 0.6) -> Location | None:

        # Сначала пробуем обычный поиск
        location = await self.get_location(location_name, vehicle_type, city, state)
        if location:
            return location

        # Парсим входные данные
        parsed_name, extracted_state = self._parse_location_input(location_name)
        if extracted_state and not state:
            state = extracted_state

        # Генерируем варианты для fuzzy поиска
        search_terms = []

        for variant in self._generate_search_variants(parsed_name):
            search_terms.append(variant)

        if city:
            search_terms.append(city)
        if state:
            search_terms.append(state)

        # Fuzzy поиск с использованием similarity
        for term in filter(None, search_terms):
            try:
                # Создаем подзапрос для поиска с similarity
                base_query = (
                    select(Location)
                    .join(DeliveryPrice)
                    .where(DeliveryPrice.vehicle_type_id == vehicle_type.id)
                )

                similarity_conditions = [
                    func.similarity(Location.name, term) > threshold,
                    func.similarity(Location.city, term) > threshold,
                    func.similarity(
                        func.regexp_replace(Location.name, r'\s+\d{5}$', '', 'g'),
                        term
                    ) > threshold,
                ]

                # Добавляем условие по штату если есть
                if state:
                    similarity_conditions.append(
                        and_(
                            func.upper(Location.state) == func.upper(state),
                            or_(*similarity_conditions[:3])
                        )
                    )

                result = await self.session.execute(
                    base_query
                    .where(or_(*similarity_conditions))
                    .order_by(desc(func.greatest(
                        func.similarity(Location.name, term),
                        func.similarity(Location.city, term),
                        func.similarity(
                            func.regexp_replace(Location.name, r'\s+\d{5}$', '', 'g'),
                            term
                        )
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
            except Exception as e:
                # Логируем ошибку для отладки
                print(f"Error in {method.__name__}: {e}")
                continue

        return None

    async def get_by_name(self, name: str) -> Location | None:
        """Поиск по точному названию"""
        result = await self.session.execute(
            select(Location).where(Location.name == name)
        )
        return result.scalar_one_or_none()
