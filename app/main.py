import os
import time
import pymysql
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import User, AccountModel
from infrastructure.database import Base, engine, SessionLocal
from pydantic import BaseModel
from contextlib import asynccontextmanager
from domain.account import Account
from infrastructure.bank_database import BankDatabase
from models import AccountModel, TransactionModel, User
from datetime import datetime

def init_db():
    from models import AccountModel, TransactionModel
    Base.metadata.create_all(bind=engine)

def wait_for_db():
    if os.getenv('WAIT_FOR_DB', 'false').lower() == 'true':
        max_retries = 10
        for _ in range(max_retries):
            try:
                conn = pymysql.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    database=os.getenv('DB_NAME')
                )
                conn.close()
                return
            except pymysql.Error:
                time.sleep(5)
        raise Exception("Could not connect to MySQL after multiple attempts")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: conectando recursos...")
    wait_for_db()
    init_db()
    yield
    print("Shutdown: limpando recursos...")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_bank_db(db: Session = Depends(get_db)):
    return BankDatabase(db)

class UserCreate(BaseModel):
    username: str
    email: str

class AccountInput(BaseModel):
    account_number: int
    pin: int
    available_balance: float
    total_balance: float
    is_admin: bool = False

class AuthInput(BaseModel):
    account_number: int
    pin: int

class TransactionInput(BaseModel):
    amount: float

class TransferInput(BaseModel):
    from_account: int
    to_account: int
    amount: float
    pin: int

class AccountUpdate(BaseModel):
    pin: Optional[int] = None
    available_balance: Optional[float] = None
    total_balance: Optional[float] = None
    is_admin: Optional[bool] = None

@app.get("/", summary="Hello World")
async def root():
    return {"message": "Hello World from ATM Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.get("/docs", include_in_schema=False)
def redirect_to_swagger():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/accounts/{account_number}")
def get_account(account_number: int, bank_db: BankDatabase = Depends(get_bank_db)):
    acc = bank_db.get_account(account_number)
    if acc is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc.to_dict()

@app.put("/accounts/{account_number}")
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

@app.post("/accounts")
def create_account(account: AccountInput, bank_db: BankDatabase = Depends(get_bank_db)):
    acc = Account(**account.dict())
    success = bank_db.add_account(acc)
    return {"created": success}

@app.post("/auth")
def authenticate(data: AuthInput, bank_db: BankDatabase = Depends(get_bank_db)):
    if bank_db.authenticate_user(data.account_number, data.pin):
        return {"status": "Authenticated"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/accounts/{account_number}/balance")
def get_balance(account_number: int, bank_db: BankDatabase = Depends(get_bank_db)):
    total = bank_db.get_total_balance(account_number)
    available = bank_db.get_available_balance(account_number)
    if total is None or available is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"total_balance": total, "available_balance": available}

@app.post("/accounts/{account_number}/credit")
def credit(account_number: int, data: TransactionInput, bank_db: BankDatabase = Depends(get_bank_db)):
    success = bank_db.credit(account_number, data.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Credit failed")
    return {"credited": True}

@app.post("/accounts/{account_number}/debit")
def debit(account_number: int, data: TransactionInput, bank_db: BankDatabase = Depends(get_bank_db)):
    success = bank_db.debit(account_number, data.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Insufficient funds or account not found")
    return {"debited": True}

@app.delete("/accounts/{account_number}")
def delete_account(account_number: int, bank_db: BankDatabase = Depends(get_bank_db)):
    success = bank_db.delete_account(account_number)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found or is admin")
    return {"deleted": True}

@app.get("/accounts/{account_number}/transactions")
def get_transactions(account_number: int, bank_db: BankDatabase = Depends(get_bank_db)):
    transactions = bank_db.get_transactions(account_number)
    if transactions is None:
        raise HTTPException(status_code=404, detail="Account not found or no transactions")
    return [t.to_dict() for t in transactions]

@app.post("/accounts/transfer")
def transfer(data: TransferInput, bank_db: BankDatabase = Depends(get_bank_db)):
    if not bank_db.authenticate_user(data.from_account, data.pin):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    success = bank_db.transfer(data.from_account, data.to_account, data.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Transfer failed: check balances or accounts")
    return {"transferred": True}

@app.get("/admin/summary")
def admin_summary(bank_db: BankDatabase = Depends(get_bank_db)):
    summary = bank_db.get_admin_summary()
    return summary
