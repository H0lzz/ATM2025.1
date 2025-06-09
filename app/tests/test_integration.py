import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

test_account = {
    "account_number": 99999,
    "pin": 1234,
    "available_balance": 1000.0,
    "total_balance": 1000.0,
    "is_admin": False
}

@pytest.fixture(scope="module")
def created_account():
    client.post("/accounts", json=test_account)
    yield test_account
    client.delete(f"/accounts/{test_account['account_number']}")

@pytest.mark.skip(reason="ignored")
def test_create_and_authenticate_account(created_account):
    auth = {
        "account_number": created_account["account_number"],
        "pin": created_account["pin"]
    }
    response = client.post("/auth", json=auth)
    assert response.status_code == 200
    assert response.json()["status"] == "Authenticated"

@pytest.mark.skip(reason="ignored")
def test_get_account_details(created_account):
    account_number = created_account["account_number"]
    response = client.get(f"/accounts/{account_number}")
    assert response.status_code == 200
    assert response.json()["account_number"] == account_number

@pytest.mark.skip(reason="ignored")
def test_credit_and_balance(created_account):
    account_number = created_account["account_number"]
    credit_amount = 500.0
    client.post(f"/accounts/{account_number}/credit", json={"amount": credit_amount})

    response = client.get(f"/accounts/{account_number}/balance")
    assert response.status_code == 200
    assert response.json()["available_balance"] >= credit_amount

@pytest.mark.skip(reason="ignored")
def test_debit_and_balance(created_account):
    account_number = created_account["account_number"]
    debit_amount = 200.0
    client.post(f"/accounts/{account_number}/debit", json={"amount": debit_amount})

    response = client.get(f"/accounts/{account_number}/balance")
    assert response.status_code == 200
    assert response.json()["available_balance"] >= 0

@pytest.mark.skip(reason="ignored")
def test_transfer(created_account):
    to_account = {
        "account_number": 88888,
        "pin": 4321,
        "available_balance": 100.0,
        "total_balance": 100.0,
        "is_admin": False
    }
    client.post("/accounts", json=to_account)

    transfer_data = {
        "from_account": created_account["account_number"],
        "to_account": to_account["account_number"],
        "amount": 100.0,
        "pin": created_account["pin"]
    }

    response = client.post("/accounts/transfer", json=transfer_data)
    assert response.status_code == 200
    assert response.json() == {"transferred": True}

    client.delete(f"/accounts/{to_account['account_number']}")

def test_get_transactions(created_account):
    account_number = created_account["account_number"]
    response = client.get(f"/accounts/{account_number}/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.skip(reason="ignored")
def test_admin_summary(created_account):
    response = client.get("/admin/summary")
    assert response.status_code == 200
    assert "total_users" in response.json()
