import asyncio
from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Optional, Callable, Any, Dict
import grpc


T = TypeVar('T')
class BaseRpcClient(Generic[T], ABC):
    def __init__(
            self,
            server_url: str,
            timeout: float = 30.0,
            max_receive_message_length: int = 4 * 1024 * 1024,
            max_send_message_length: int = 4 * 1024 * 1024,
            compression: Optional[grpc.Compression] = None
    ):
        self.server_url = server_url
        self.timeout = timeout
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[T] = None

        self.channel_options = [
            ('grpc.max_receive_message_length', max_receive_message_length),
            ('grpc.max_send_message_length', max_send_message_length),
        ]
        self.compression = compression

    @abstractmethod
    def _create_stub(self, channel: grpc.aio.Channel) -> T:
        pass

    async def connect(self):
        if self.channel is not None:
            return
        try:
            self.channel = grpc.aio.insecure_channel(
                self.server_url,
                options=self.channel_options
            )
            self.stub = self._create_stub(self.channel)

            await asyncio.wait_for(
                self.channel.channel_ready(),
                timeout=self.timeout
            )
        except Exception as e:
            await self.disconnect()
            raise

    async def disconnect(self):
        if self.channel:
            try:
                await self.channel.close()
            finally:
                self.channel = None
                self.stub = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    def _ensure_connected(self):
        if not self.channel or not self.stub:
            raise RuntimeError(
                "RPC клиент не подключен. Используйте async with или вызовите connect()"
            )

    async def _execute_request(
            self,
            method: Callable,
            request: Any,
            metadata: Optional[Dict[str, str]] = None,
            timeout: Optional[float] = None
    ) -> Any:
        self._ensure_connected()

        rpc_metadata = []
        if metadata:
            rpc_metadata = [(key, value) for key, value in metadata.items()]

        request_timeout = timeout or self.timeout


        response = await asyncio.wait_for(
            method(
                request,
                metadata=rpc_metadata,
                compression=self.compression
            ),
            timeout=request_timeout
        )

        return response