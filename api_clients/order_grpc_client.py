# api_clients/order_grpc_client.py

import grpc
from config.settings import GRPC_SERVER

# Dummy import for generated proto stubs
# from . import order_pb2, order_pb2_grpc

# Client gRPC để gọi các API liên quan đến đơn hàng (Order)
class OrderGrpcClient:
    def __init__(self, server=GRPC_SERVER):
        # Khởi tạo channel kết nối tới server gRPC
        self.channel = grpc.insecure_channel(server)
        # self.stub = order_pb2_grpc.OrderServiceStub(self.channel)  # Stub cho service thực tế

    def get_order(self, order_id):
        # Hàm lấy thông tin đơn hàng theo order_id (hiện tại là dummy)
        # request = order_pb2.GetOrderRequest(order_id=order_id)
        # return self.stub.GetOrder(request)
        return {"order_id": order_id, "status": "DUMMY"}

    def close(self):
        # Đóng channel khi không sử dụng nữa
        self.channel.close() 