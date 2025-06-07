from sqlalchemy import Column, Integer, String, Float, Boolean
from infrastructure.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(20), unique=True)
    owner_name = Column(String(100))
    balance = Column(Float, default=0.0)
    pin = Column(String(4))
    is_admin = Column(Boolean, default=False)