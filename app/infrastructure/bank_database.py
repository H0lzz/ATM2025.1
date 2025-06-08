from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal
from models import AccountModel, TransactionModel, TransactionType
from domain.account import Account
from datetime import datetime

class BankDatabase:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_account(self, account_number):
        print("[DEBUG] Buscando conta no banco de dados...")
        acc = self.db.query(AccountModel).filter_by(account_number=account_number).first()
        return Account.from_dict(acc.to_dict()) if acc else None

    def authenticate_user(self, account_number, pin):
        acc = self.db.query(AccountModel).filter_by(account_number=account_number, pin=pin).first()
        return acc is not None

    def is_admin(self, account_number):
        acc = self.db.query(AccountModel).filter_by(account_number=account_number).first()
        return acc.is_admin if acc else False

    def add_account(self, account):
        if not self.get_account(account.account_number):
            acc = AccountModel(**account.to_dict())
            self.db.add(acc)
            self.db.commit()
            return True
        return False

    def delete_account(self, account_number):
        acc = self.db.query(AccountModel).filter_by(account_number=account_number).first()
        if acc and not acc.is_admin:
            self.db.delete(acc)
            self.db.commit()
            return True
        return False

    def update_account(self, account_number, new_data):
        acc = self.db.query(AccountModel).filter_by(account_number=account_number).first()
        if acc:
            for key, value in new_data.items():
                if key != 'account_number' and hasattr(acc, key):
                    setattr(acc, key, value)
            self.db.commit()
            return True
        return False

    def get_all_accounts(self):
        accounts = self.db.query(AccountModel).all()
        return [Account.from_dict(acc.__dict__).to_dict() for acc in accounts]

    def get_available_balance(self, account_number):
        acc = self.db.query(AccountModel).filter_by(account_number=account_number).first()
        return acc.available_balance if acc else None

    def get_total_balance(self, account_number):
        acc = self.db.query(AccountModel).filter_by(account_number=account_number).first()
        return acc.total_balance if acc else None
    
    def record_transaction(self, account_id, trans_type: str, amount: float):
        transaction = TransactionModel(
            account_id=account_id,
            type=TransactionType(trans_type),
            amount=amount,
            timestamp=datetime.now()
        )
        self.db.add(transaction)
        self.db.commit()

    def credit(self, account_number, amount):
        acc = self.db.query(AccountModel).filter_by(account_number=account_number).first()
        if acc:
            acc.total_balance += amount
            acc.available_balance += amount
            self.db.commit()
            self.record_transaction(account_id=acc.id, trans_type="deposit", amount=amount)
            return True
        return False

    def debit(self, account_number, amount):
        acc = self.db.query(AccountModel).filter_by(account_number=account_number).first()
        if acc and acc.available_balance >= amount:
            acc.available_balance -= amount
            acc.total_balance -= amount
            self.db.commit()
            self.record_transaction(account_id=acc.id, trans_type="withdrawal", amount=amount)
            return True
        return False
