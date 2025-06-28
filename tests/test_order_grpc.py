# tests/test_order_grpc.py

def test_get_order_grpc(grpc_client):
    order_id = "12345"
    response = grpc_client.get_order(order_id)
    assert response["order_id"] == order_id
    assert response["status"] == "DUMMY" 