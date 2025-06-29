# tests/test_order_grpc.py

import pytest
from api_clients.order_grpc_client import OrderGrpcClient

@pytest.mark.grpc
@pytest.mark.regression
def test_get_order_grpc():
    """Test gRPC lấy thông tin order"""
    grpc_client = OrderGrpcClient()
    
    # Test get order
    order = grpc_client.get_order("ORDER_123")
    
    # Kiểm tra response
    assert order is not None
    assert order["order_id"] == "ORDER_123"
    assert order["status"] in ["pending", "completed", "cancelled"] 