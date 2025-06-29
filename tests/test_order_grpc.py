# tests/test_order_grpc.py

import pytest
from api_clients.order_grpc_client import OrderGrpcClient

@pytest.mark.grpc
@pytest.mark.regression
def test_get_order_grpc():
    """Test gRPC order service"""
    client = OrderGrpcClient()
    order = client.get_order(1)
    
    # Kiểm tra order có các field cần thiết
    assert "order_id" in order
    assert "status" in order
    
    # Kiểm tra status là DUMMY (mock response)
    assert order["status"] == "DUMMY"
    
    # Kiểm tra các field khác
    assert isinstance(order["order_id"], int) 