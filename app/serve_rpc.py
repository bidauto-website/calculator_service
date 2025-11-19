import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'rpc_server', 'gen', 'python'))
import grpc
import signal

from grpc_health.v1 import health_pb2_grpc, health_pb2
from grpc_reflection.v1alpha import reflection

from app.rpc_client_server.calulator_rpc import CalculatorRpc
from app.rpc_client_server.detailed_info_rpc import DetailedInfoRpc
from app.rpc_client_server.gen.python.calculator.v1 import calculator_pb2, calculator_pb2_grpc
from app.rpc_client_server.health import HealthCheckServicer



from config import settings, Environment
from core.logger import logger


class GracefulServer:
    def __init__(self):
        self.server = None
        self.shutdown_event = asyncio.Event()

    async def setup_server(self):
        self.server = grpc.aio.server()

        listen_addr = f'[::]:{settings.GRPC_SERVER_PORT}'


        self.server.add_insecure_port(listen_addr)

        calculator_pb2_grpc.add_CalculatorServiceServicer_to_server(CalculatorRpc(), self.server)
        calculator_pb2_grpc.add_DetailedInfoServiceServicer_to_server(DetailedInfoRpc(), self.server)
        health_pb2_grpc.add_HealthServicer_to_server(HealthCheckServicer(), self.server)

        if settings.ENVIRONMENT == Environment.DEVELOPMENT:
            try:
                service_names = [
                    calculator_pb2.DESCRIPTOR.services_by_name['CalculatorService'].full_name,
                    calculator_pb2.DESCRIPTOR.services_by_name['DetailedInfoService'].full_name,
                    health_pb2.DESCRIPTOR.services_by_name['Health'].full_name,
                    reflection.SERVICE_NAME,
                ]
                reflection.enable_server_reflection(service_names, self.server)
                logger.info("🔍 gRPC Reflection enabled for development")
            except Exception as e:
                logger.warning(f"⚠️  Failed to enable reflection: {e}")

        logger.info(f"🚀 gRPC Server configured on {listen_addr}")

    def setup_signal_handlers(self):

        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            asyncio.create_task(self.shutdown())

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

    async def shutdown(self):
        if not self.shutdown_event.is_set():
            self.shutdown_event.set()

    async def serve(self):
        await self.setup_server()
        self.setup_signal_handlers()

        await self.server.start()
        logger.info("✅ gRPC Server started successfully")

        try:
            await self.shutdown_event.wait()
        except asyncio.CancelledError:
            logger.info("Server cancelled")
        finally:
            logger.info("Shutting down server...")
            await self.server.stop(grace=10.0)
            logger.info("Server stopped")


async def main():
    server = GracefulServer()
    try:
        await server.serve()
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
