import os
import sys

import grpc

from app.config import settings
from app.rpc_client.base_client import BaseRpcClient, T

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gen', 'python'))

from app.rpc_client.gen.python.auction.v1 import lot_pb2_grpc, lot_pb2


class ApiRpcClient(BaseRpcClient[lot_pb2_grpc.LotServiceStub]):
    def __init__(self):
        super().__init__(server_url=settings.RPC_API_URL)

    async def __aenter__(self):
        await self.connect()
        return self

    def _create_stub(self, channel: grpc.aio.Channel) -> T:
        return lot_pb2_grpc.LotServiceStub(channel)

    async def get_lot_by_vin_or_lot_id(self, vin_or_lot_id: str, site: str = None) -> lot_pb2.GetLotByVinOrLotResponse:
        data = lot_pb2.GetLotByVinOrLotRequest(vin_or_lot_id=vin_or_lot_id, site=site)
        return await self._execute_request(self.stub.GetLotByVinOrLot, data)

    async def get_current_bid(self, lot_id: int, site: str) -> lot_pb2.GetCurrentBidResponse:
        data = lot_pb2.GetCurrentBidRequest(lot_id=lot_id, site=site)
        return await self._execute_request(self.stub.GetCurrentBid, data)

    async def get_sale_history(self, lot_id: int, site: str) -> lot_pb2.GetSaleHistoryResponse:
        data = lot_pb2.GetSaleHistoryRequest(lot_id=lot_id, site=site)
        return await self._execute_request(self.stub.GetSaleHistory, data)
