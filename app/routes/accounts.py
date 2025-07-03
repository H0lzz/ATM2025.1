from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from domain.account import Account
from infrastructure.bank_database import BankDatabase
from models import AccountModel
from infrastructure.database import SessionLocal

router = APIRouter(prefix="/accounts", tags=["accounts"])

class AccountInput(BaseModel):
    account_number: int
    pin: int
    available_balance: float
    total_balance: float
    is_admin: bool = False

class AccountUpdate(BaseModel):
    pin: Optional[int] = None
    available_balance: Optional[float] = None
    total_balance: Optional[float] = None
    is_admin: Optional[bool] = None

class TransactionInput(BaseModel):
    amount: float

class TransferInput(BaseModel):
    from_account: int
    to_account: int
    amount: float
    pin: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_bank_db(db: Session = Depends(get_db)):
    return BankDatabase(db)

@router.post("")
def create_account(account: AccountInput, bank_db: BankDatabase = Depends(get_bank_db)):
    acc = Account(**account.dict())
    success = bank_db.add_account(acc)
    return {"created": success}

@router.get("/{account_number}")
def get_account(account_number: int, bank_db: BankDatabase = Depends(get_bank_db)):
    acc = bank_db.get_account(account_number)
    if acc is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc.to_dict()

@router.put("/{account_number}")
def update_account(account_number: int, update: AccountUpdate, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if update.pin is not None:
        account.pin = update.pin
    if update.available_balance is not None:
        account.available_balance = update.available_balance
    if update.total_balance is not None:
        account.total_balance = update.total_balance
    if update.is_admin is not None:
        account.is_admin = update.is_admin

    db.commit()
    db.refresh(account)
    return account.to_dict()

@router.delete("/{account_number}")
def delete_account(account_number: int, bank_db: BankDatabase = Depends(get_bank_db)):
    success = bank_db.delete_account(account_number)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found or is admin")
    return {"deleted": True}

@router.post("/{account_number}/credit")
def credit(account_number: int, data: TransactionInput, bank_db: BankDatabase = Depends(get_bank_db)):
    success = bank_db.credit(account_number, data.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Credit failed")
    return {"credited": True}

@router.post("/{account_number}/debit")
def debit(account_number: int, data: TransactionInput, bank_db: BankDatabase = Depends(get_bank_db)):
    success = bank_db.debit(account_number, data.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Debit failed")
    return {"debited": True}

@router.get("/{account_number}/balance")
def get_balance(account_number: int, bank_db: BankDatabase = Depends(get_bank_db)):
    total = bank_db.get_total_balance(account_number)
    available = bank_db.get_available_balance(account_number)
    return {"total_balance": total, "available_balance": available}

@router.delete("/{account_number}")
def delete_account(account_number: int, bank_db: BankDatabase = Depends(get_bank_db)):
    success = bank_db.delete_account(account_number)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found or is admin")
    return {"deleted": True}

@router.get("/{account_number}/transactions")
def get_transactions(account_number: int, bank_db: BankDatabase = Depends(get_bank_db)):
    transactions = bank_db.get_transactions(account_number)
    if transactions is None:
        raise HTTPException(status_code=404, detail="No transactions found")
    return [t.to_dict() for t in transactions]
