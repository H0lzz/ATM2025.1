import pytest
from fastapi.testclient import TestClient
from main import app
from infrastructure.database import Base, engine

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # Limpa após os testes
    Base.metadata.drop_all(bind=engine)