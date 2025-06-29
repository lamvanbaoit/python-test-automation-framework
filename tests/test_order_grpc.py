# tests/test_order_grpc.py

# Test kiểm thử lấy thông tin đơn hàng qua gRPC client

def test_get_order_grpc(grpc_client):
    order_id = "12345"  # ID đơn hàng mẫu
    response = grpc_client.get_order(order_id)
    # Kiểm tra response trả về đúng order_id và status dummy
    assert response["order_id"] == order_id
    assert response["status"] == "DUMMY" 