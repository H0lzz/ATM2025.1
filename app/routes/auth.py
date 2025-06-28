from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from infrastructure.bank_database import BankDatabase

router = APIRouter(prefix="/auth", tags=["auth"])

class AuthInput(BaseModel):
    account_number: int
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
def authenticate(data: AuthInput, bank_db: BankDatabase = Depends(get_bank_db)):
    if bank_db.authenticate_user(data.account_number, data.pin):
        return {"status": "Authenticated"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/logs")
def get_auth_logs():
    return {
        "logs": [
            {"account": 999, "method": "biometric", "success": False, "timestamp": "2025-06-07T12:00:00"},
            {"account": 999, "method": "pin", "success": True, "timestamp": "2025-06-07T12:01:00"},
        ]
    }
