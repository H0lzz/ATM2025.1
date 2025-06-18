import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.skip(reason="Implementação pendente - TDD")
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from ATM Backend!"}

@pytest.mark.skip(reason="ignored")
def test_health_check():
    """Teste do endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}