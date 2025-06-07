import os
import time
import pymysql
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import User, Account
from infrastructure.database import Base, engine, SessionLocal
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.bank_database import BankDatabase
from domain.transaction import Withdrawal, Deposit
from domain.schemas import AccountCreate, TransactionRequest, BalanceResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: conectando recursos...")
    wait_for_db()
    init_db()
    yield
    print("Shutdown: limpando recursos...")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

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

def init_db():
    print("Criando tabelas no banco (se não existirem)...")
    Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    username: str
    email: str

@app.get("/", summary="Hello World")
async def root():
    return {"message": "Hello World from ATM Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.get("/docs", include_in_schema=False)
def redirect_to_swagger():
    from fastapi.responsse import RedirectResponse
    return RedirectResponse(url="/docs")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.post("/login")
async def login(account_number: str, pin: str, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_number == account_number).first()
    if not account or account.pin != pin:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"message": "Login bem-sucedido", "is_admin": account.is_admin}

@app.post("/accounts")
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    # Converta para sua classe BankDatabase existente
    bank_db = BankDatabase()
    if bank_db.get_account(account.account_number):
        raise HTTPException(status_code=400, detail="Account already exists")
    
    # Crie a conta usando sua lógica existente
    new_account = Account(
        account_number=account.account_number,
        pin=account.pin,
        balance=account.initial_balance,
        is_admin=account.is_admin
    )
    db.add(new_account)
    db.commit()
    return {"message": "Account created"}

@app.post("/accounts/{account_number}/withdraw")
def withdraw(account_number: str, transaction: TransactionRequest, db: Session = Depends(get_db)):
    bank_db = BankDatabase()
    account = bank_db.get_account(account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Use sua classe Withdrawal existente
    withdrawal = Withdrawal(account_number, bank_db, transaction.amount)
    result = withdrawal.execute()
    
    if "Insufficient funds" in result:
        raise HTTPException(status_code=400, detail=result)
    
    return {"message": result}

@app.post("/accounts/{account_number}/deposit")
def deposit(account_number: str, transaction: TransactionRequest, db: Session = Depends(get_db)):
    bank_db = BankDatabase(db)
    account = bank_db.get_account(account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Use sua classe Deposit existente
    deposit = Deposit(account_number, bank_db, transaction.amount)
    result = deposit.execute()
    
    return {"message": result}

@app.get("/accounts/{account_number}/balance", response_model=BalanceResponse)
def get_balance(account_number: str, db: Session = Depends(get_db)):
    bank_db = BankDatabase(db)  # Use sua classe BankDatabase
    account = bank_db.get_account(account_number)
    
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    return {
        "account_number": account.account_number,
        "balance": account.balance,
        "currency": "BRL"  # Exemplo: pode ser dinâmico
    }

class CreateAccountRequest(BaseModel):
    account_number: str
    owner_name: str
    pin: str
    initial_balance: float = 0.0
    is_admin: bool = False

@app.post("/admin/accounts")
async def create_account(request: CreateAccountRequest, db: Session = Depends(get_db)):
    if db.query(Account).filter(Account.account_number == request.account_number).first():
        raise HTTPException(status_code=400, detail="Conta já existe")
    
    new_account = Account(
        account_number=request.account_number,
        owner_name=request.owner_name,
        pin=request.pin,
        balance=request.initial_balance,
        is_admin=request.is_admin
    )
    db.add(new_account)
    db.commit()
    return {"message": "Conta criada com sucesso", "account_number": request.account_number}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)