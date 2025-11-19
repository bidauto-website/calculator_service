from typing import Type, TypeVar

import grpc
from sqlalchemy.exc import SQLAlchemyError

from app.core.logger import logger
from app.database.db.session import get_db_context
from app.database.models import Location, Terminal, Destination, FeeType
from app.rpc_client_server.gen.python.calculator.v1 import calculator_pb2_grpc, calculator_pb2
from app.rpc_client_server.gen.python.calculator.v1.calculator_pb2 import (
    GetDetailedFeeTypeResponse,
    GetDetailedLocationResponse,
    GetDetailedTerminalResponse,
    GetDetailedDestinationResponse,
)

ModelType = TypeVar("ModelType")


class DetailedInfoRpc(calculator_pb2_grpc.DetailedInfoServiceServicer):


    @staticmethod
    async def _fetch_entity(
        model: Type[ModelType],
        obj_id: int,
        entity_name: str,
        context,
    ) -> ModelType | None:
        if obj_id <= 0:
            message = f"{entity_name} id must be greater than 0"
            logger.warning(message)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(message)
            return None

        try:
            async with get_db_context() as db:
                entity = await db.get(model, obj_id)
                if entity:
                    logger.debug("Found %s with id=%s", entity_name, obj_id)
                    return entity

            message = f"{entity_name} {obj_id} not found"
            logger.info(message)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(message)
            return None
        except SQLAlchemyError as exc:
            logger.error("Database error while fetching %s %s: %s", entity_name, obj_id, exc, exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to fetch {entity_name.lower()}")
            return None
        except Exception as exc:
            logger.exception("Unexpected error while fetching %s %s: %s", entity_name, obj_id, exc)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to fetch {entity_name.lower()}")
            return None

    async def GetDetailedLocation(self, request: calculator_pb2.GetDetailedLocationRequest, context):
        logger.info("GetDetailedLocation request received: id=%s", request.id)
        location = await self._fetch_entity(Location, request.id, "Location", context)
        if not location:
            return GetDetailedLocationResponse()

        return GetDetailedLocationResponse(
            name=location.name or "",
            city=location.city or "",
            state=location.state or "",
            postal_code=location.postal_code or "",
            email=location.email or "",
        )

    async def GetDetailedTerminal(self, request: calculator_pb2.GetDetailedTerminalRequest, context):
        logger.info("GetDetailedTerminal request received: id=%s", request.id)
        terminal = await self._fetch_entity(Terminal, request.id, "Terminal", context)
        if not terminal:
            return GetDetailedTerminalResponse()

        return GetDetailedTerminalResponse(name=terminal.name or "")

    async def GetDetailedDestination(self, request: calculator_pb2.GetDetailedDestinationRequest, context):
        logger.info("GetDetailedDestination request received: id=%s", request.id)
        destination = await self._fetch_entity(Destination, request.id, "Destination", context)
        if not destination:
            return GetDetailedDestinationResponse()

        return GetDetailedDestinationResponse(
            name=destination.name or "",
            is_default=bool(destination.is_default),
        )
    async def GetDetailedFeeType(self, request: calculator_pb2.GetDetailedFeeTypeRequest, context):
        logger.info("GetDetailedFeeType request received: id=%s", request.id)
        fee_type_obj = await self._fetch_entity(FeeType, request.id, "FeeType", context)
        if not fee_type_obj:
            return GetDetailedFeeTypeResponse()

        return GetDetailedFeeTypeResponse(
            auction=fee_type_obj.auction.value if fee_type_obj.auction else "",
            fee_type=fee_type_obj.fee_type.value if fee_type_obj.fee_type else "",
        )