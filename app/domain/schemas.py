from pydantic import BaseModel

class AccountCreate(BaseModel):
    account_number: str
    pin: str
    initial_balance: float = 0.0
    is_admin: bool = False

class TransactionRequest(BaseModel):
    amount: float


class BalanceResponse(BaseModel):
    account_number: str
    balance: float
    currency: str