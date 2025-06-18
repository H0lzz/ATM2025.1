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

class Branch(Base):
    __tablename__ = "branch"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)

class Card(Base):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    card_number = Column(String(16), unique=True, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    success = Column(Boolean, default=False)
    ip_address = Column(String(45))

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    performed_by = Column(String(50))

class CashDispenser(Base):
    __tablename__ = "cash_dispenser"

    id = Column(Integer, primary_key=True, index=True)
    denomination = Column(Integer, nullable=False)
    quantity = Column(Integer, default=0)

class NotificationType(enum.Enum):
    email = "email"
    sms = "sms"
    push = "push"

class Notifier(Base):
    __tablename__ = "notifier"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    destination = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
