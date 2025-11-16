
from grpc_health.v1 import health_pb2_grpc, health_pb2


class HealthCheckServicer(health_pb2_grpc.HealthServicer):
    """Health check сервис для мониторинга"""

    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING
        )

    def Watch(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING
        )