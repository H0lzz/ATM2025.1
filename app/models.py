from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, text
from sqlalchemy.sql import func
import enum
from infrastructure.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)

class AccountModel(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_number = Column(Integer, unique=True, index=True, nullable=False)
    pin = Column(Integer, nullable=False)
    available_balance = Column(Float, default=0.0)
    total_balance = Column(Float, default=0.0)
    is_admin = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "account_number": self.account_number,
            "pin": self.pin,
            "available_balance": self.available_balance,
            "total_balance": self.total_balance,
            "is_admin": self.is_admin,
        }

class TransactionType(enum.Enum):
    deposit = "deposit"
    withdraw = "withdraw"

class TransactionModel(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "type": self.type.value,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
