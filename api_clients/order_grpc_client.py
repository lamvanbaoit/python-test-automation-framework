# api_clients/order_grpc_client.py

import grpc
from config.settings import GRPC_SERVER

# Dummy import for generated proto stubs
# from . import order_pb2, order_pb2_grpc

class OrderGrpcClient:
    def __init__(self, server=GRPC_SERVER):
        self.channel = grpc.insecure_channel(server)
        # self.stub = order_pb2_grpc.OrderServiceStub(self.channel)

    def get_order(self, order_id):
        # Dummy implementation
        # request = order_pb2.GetOrderRequest(order_id=order_id)
        # return self.stub.GetOrder(request)
        return {"order_id": order_id, "status": "DUMMY"}

    def close(self):
        self.channel.close() 