import time
from typing import TYPE_CHECKING

import grpc

from app.core.logger import logger
from app.database.db.session import get_db_context
from app.enums.auction import AuctionEnum
from app.enums.fee_type import FeeTypeEnum
from app.enums.vehicle_type import VehicleTypeEnum
from app.rpc_client_server.auction_api import ApiRpcClient
from app.rpc_client_server.gen.python.calculator.v1 import calculator_pb2_grpc, calculator_pb2
from app.rpc_client_server.gen.python.calculator.v1.calculator_pb2 import CalculatorOut, GetCalculatorWithDataResponse, \
    DefaultCalculator, EUCalculator, City, AdditionalFeesOut, SpecialFee, VATs, GetCalculatorWithoutDataResponse, \
    GetCalculatorWithDataBatchResponse, CalculatorBatchItem
from app.services.calculator.calculator_service import CalculatorService
from app.services.calculator.exceptions import NotFoundError

if TYPE_CHECKING:
    from app.services.calculator.types import City as PydanticCity
    from app.services.calculator.types import SpecialFee as PydanticSpecialFee


class CalculatorRpc(calculator_pb2_grpc.CalculatorServiceServicer):

    @staticmethod
    def transform_to_proto(data, proto_class):
        logger.debug(f"Transforming data to proto {proto_class.__name__}, data count: {len(data) if data else 0}")
        try:
            if not data:
                logger.debug(f"No data to transform for {proto_class.__name__}")
                return []
            result = [proto_class(price=item.price, name=item.name) for item in data]
            logger.debug(f"Successfully transformed {len(result)} items to {proto_class.__name__}")
            return result
        except (AttributeError, TypeError) as e:
            logger.error(f"Error transforming data to proto {proto_class.__name__}: {e}")
            raise ValueError(f"Invalid data format for {proto_class.__name__}")

    def _create_calculator_out(self, calc) -> CalculatorOut:
        logger.debug("Creating CalculatorOut from calculation result")
        try:
            c = calc.calculator
            logger.debug(f"Processing calculator with broker_fee: {c.broker_fee}")

            transport = self.transform_to_proto(c.transportation_price, City)
            ocean = self.transform_to_proto(c.ocean_ship, City)

            additional = AdditionalFeesOut(
                summ=c.additional.summ if c.additional else 0,
                fees=self.transform_to_proto(
                    c.additional.fees if c.additional else [],
                    SpecialFee
                ),
                auction_fee=c.additional.auction_fee if c.additional else 0,
                internet_fee=c.additional.internet_fee if c.additional else 0,
                live_fee=c.additional.live_fee if c.additional else 0,
            )
            logger.debug(f"Created additional fees with summ: {additional.summ}")

            base = dict(
                broker_fee=c.broker_fee or 0,
                transportation_price=transport,
                ocean_ship=ocean,
                additional=additional
            )

            eu_calculator_exists = calc.eu_calculator is not None
            logger.debug(f"EU calculator exists: {eu_calculator_exists}")

            result = CalculatorOut(
                calculator=DefaultCalculator(
                    **base,
                    totals=self.transform_to_proto(c.totals, City),
                    auction_fee=c.auction_fee or 0,
                    live_fee=c.live_fee or 0,
                    internet_fee=c.internet_fee or 0,
                ),
                eu_calculator=EUCalculator(
                    **base,
                    totals=self.transform_to_proto(
                        calc.eu_calculator.totals if calc.eu_calculator else [],
                        City
                    ),
                    vats=VATs(
                        vats=self.transform_to_proto(
                            calc.eu_calculator.vats.vats if calc.eu_calculator and calc.eu_calculator.vats else [],
                            City
                        ),
                        eu_vats=self.transform_to_proto(
                            calc.eu_calculator.vats.eu_vats if calc.eu_calculator and calc.eu_calculator.vats else [],
                            City
                        ),
                    ),
                    custom_agency=calc.eu_calculator.custom_agency if calc.eu_calculator else 0,
                )
            )
            logger.info("Successfully created CalculatorOut")
            return result
        except Exception as e:
            logger.error(f"Error creating CalculatorOut: {e}", exc_info=True)
            raise

    async def _calculate_and_respond(self, params, context, response_class):
        logger.info(f"Starting calculation with params: {params}")
        try:
            async with get_db_context() as db:
                logger.debug("Database connection established")
                calculator_service = CalculatorService(db=db, **params)
                logger.debug("CalculatorService instance created")
                result = await calculator_service.calculate()
                logger.info("Calculation completed successfully")

                response = response_class(
                    data=self._create_calculator_out(result.calculator_in_dollars),
                    message='Success',
                    success=True,
                )
                logger.debug("Response created successfully")
                return response
        except NotFoundError as e:
            logger.warning(f"Not found error: {e.message}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(e.message)
            return response_class(
                message=e.message,
                success=False
            )
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return response_class(
                message=str(e),
                success=False
            )
        except Exception as e:

            logger.exception(f"Unexpected error in calculation: {e}", )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error during calculation")
            return response_class(
                message="Internal server error",
                success=False
            )

    def _safe_enum_conversion(self, value, enum_class, field_name: str):
        logger.debug(f"Converting {field_name} value '{value}' to {enum_class.__name__}")
        try:
            result = enum_class(value)
            logger.debug(f"Successfully converted {field_name} to {result}")
            return result
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to convert {field_name}: {value} to {enum_class.__name__}")
            raise ValueError(f"Invalid {field_name}: {value}. Expected one of {[e.value for e in enum_class]}")

    def get_params_from_request(self, request: calculator_pb2.GetCalculatorWithDataRequest):
        params = dict(
            price=request.price,
            auction=self._safe_enum_conversion(request.auction.upper(), AuctionEnum, "auction"),
            fee_type=self._safe_enum_conversion(request.fee_type, FeeTypeEnum,
                                                "fee_type") if request.fee_type else None,
            location=request.location,
            vehicle_type=self._safe_enum_conversion(request.vehicle_type, VehicleTypeEnum, "vehicle_type"),
            destination=request.destination if request.destination else None,
        )
        return params

    async def GetCalculatorWithData(self, request: calculator_pb2.GetCalculatorWithDataRequest, context):
        logger.info(
            f"GetCalculatorWithData called with price: {request.price}, auction: {request.auction}, location: {request.location}")
        try:
            if request.price < -1:
                logger.warning(f"Invalid price provided: {request.price}")
                raise ValueError("Price must be greater than -1")

            if not request.location:
                logger.warning("Location not provided in request")
                raise ValueError("Location is required")

            logger.debug(
                f"Validating request parameters: auction={request.auction}, fee_type={request.fee_type}, vehicle_type={request.vehicle_type}")

            params = self.get_params_from_request(request)

            logger.info(f"Parameters validated successfully for GetCalculatorWithData: {params}")
            return await self._calculate_and_respond(
                params,
                context,
                GetCalculatorWithDataResponse
            )

        except ValueError as e:
            logger.warning(f"Validation error in GetCalculatorWithData: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return GetCalculatorWithDataResponse(
                message=str(e),
                success=False
            )
        except Exception as e:
            logger.error(f"Unexpected error in GetCalculatorWithData: {e}", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return GetCalculatorWithDataResponse(
                message="Internal server error",
                success=False
            )

    async def GetCalculatorWithDataBatch(self, request, context):
        logger.info(f"GetCalculatorWithDataBatch called with {len(request.data)} requests")

        start = time.time()
        try:
            responses = []

            for i, req_item in enumerate(request.data):
                item_start = time.time()

                params = self.get_params_from_request(req_item.data)
                response = await self._calculate_and_respond(
                    params,
                    context,
                    GetCalculatorWithDataResponse
                )

                item_time = time.time() - item_start
                logger.info(f"Item {i} (lot_id={req_item.lot_id}) took {item_time:.3f}s")

                if context.code() != grpc.StatusCode.OK:
                    logger.error(f"Error in batch item with lot_id {req_item.lot_id}: {context.details()}")
                    context.set_code(grpc.StatusCode.OK)
                    context.set_details("")
                    continue

                responses.append(CalculatorBatchItem(calculator=response.data, lot_id=req_item.lot_id))

            total_time = time.time() - start
            logger.info(f"Total batch time: {total_time:.3f}s")

            return GetCalculatorWithDataBatchResponse(data=responses)

        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return GetCalculatorWithDataBatchResponse()

    async def GetCalculatorWithoutData(self, request, context):
        logger.info(
            f"GetCalculatorWithoutData called with price: {request.price}, lot_id: {request.lot_id}, auction: {request.auction}")
        try:
            if request.price <= 0:
                logger.warning(f"Invalid price provided: {request.price}")
                raise ValueError("Price must be greater than 0")

            if not request.lot_id:
                logger.warning("Lot ID not provided in request")
                raise ValueError("Lot ID is required")

            auction_enum = self._safe_enum_conversion(request.auction, AuctionEnum, "auction")
            logger.debug(f"Auction enum converted: {auction_enum}")

            lot = None
            try:
                logger.info(f"Fetching lot data for lot_id: {request.lot_id}, auction: {request.auction}")
                async with ApiRpcClient() as client:
                    lot = await client.get_lot_by_vin_or_lot_id(request.lot_id, request.auction)
                logger.info(f"Successfully fetched lot data for lot_id: {request.lot_id}")
            except grpc.aio.AioRpcError as e:
                logger.error(f"RPC error when fetching lot data: {e.code()}: {e.details()}")
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details(f"Lot {request.lot_id} not found")
                    return GetCalculatorWithoutDataResponse(
                        message=f"Lot {request.lot_id} not found",
                        success=False
                    )
                elif e.code() == grpc.StatusCode.UNAVAILABLE:
                    context.set_code(grpc.StatusCode.UNAVAILABLE)
                    context.set_details("External service unavailable")
                    return GetCalculatorWithoutDataResponse(
                        message="Cannot fetch lot data: service unavailable",
                        success=False
                    )
                else:
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details("Failed to fetch lot data")
                    return GetCalculatorWithoutDataResponse(
                        message="Failed to fetch lot data",
                        success=False
                    )
            except Exception as e:
                logger.error(f"Unexpected error when fetching lot data: {e}", exc_info=True)
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to fetch lot data")
                return GetCalculatorWithoutDataResponse(
                    message="Failed to fetch lot data",
                    success=False
                )

            if not lot or not lot.lot or len(lot.lot) == 0:
                logger.warning(f"No lot data found for lot_id: {request.lot_id}")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"No data found for lot {request.lot_id}")
                return GetCalculatorWithoutDataResponse(
                    message=f"No data found for lot {request.lot_id}",
                    success=False
                )

            try:
                lot_item = lot.lot[0]
                logger.debug(f"Processing lot item with location: {lot_item.location}")

                if not lot_item.location:
                    logger.error("Lot location is empty")
                    raise ValueError("Lot location is empty")

                vehicle_type = VehicleTypeEnum.CAR
                if hasattr(lot_item, 'vehicle_type'):
                    if lot_item.vehicle_type and lot_item.vehicle_type.lower() == 'automobile':
                        vehicle_type = VehicleTypeEnum.CAR
                    else:
                        vehicle_type = VehicleTypeEnum.MOTO
                logger.debug(f"Determined vehicle type: {vehicle_type}")

                params = dict(
                    price=request.price,
                    auction=auction_enum,
                    location=lot_item.location,
                    vehicle_type=vehicle_type
                )
                logger.info(f"Parameters prepared for calculation: {params}")

            except (IndexError, AttributeError) as e:
                logger.error(f"Error parsing lot data: {e}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Invalid lot data format")
                return GetCalculatorWithoutDataResponse(
                    message="Invalid lot data format",
                    success=False
                )

            return await self._calculate_and_respond(
                params,
                context,
                GetCalculatorWithoutDataResponse
            )

        except ValueError as e:
            logger.warning(f"Validation error in GetCalculatorWithoutData: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return GetCalculatorWithoutDataResponse(
                message=str(e),
                success=False
            )
        except Exception as e:
            logger.error(f"Unexpected error in GetCalculatorWithoutData: {e}", exc_info=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return GetCalculatorWithoutDataResponse(
                message="Internal server error",
                success=False
            )