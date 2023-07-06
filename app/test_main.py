from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "Hello World"}

def test_get_endpoint():
    response = client.get("/items/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"item_id": 1, "name": "Item 1"}

def test_create_post():
    # Define the request payload
    payload = {
        "id": 1,
        "title": "Test Post",
        "content": "This is a test post."
    }

    # Send a POST request to the endpoint
    response = client.post("/posts", json=payload)

    # Verify the response status code
    assert response.status_code == 200

    # Verify the response JSON content
    assert response.json() == payload