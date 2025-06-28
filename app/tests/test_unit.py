import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize("path, expected_status, expected_json", [
    ("/", 200, {"message": "Hello World from ATM Backend!"}),
    ("/health", 200, {"status": "OK"}),
])

@pytest.mark.skip(reason="ignored")
def test_basic_routes(path, expected_status, expected_json):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_json
