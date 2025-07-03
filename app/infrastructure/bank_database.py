from sqlalchemy.orm import Session
from sqlalchemy import func
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
            self.record_transaction(account_id=acc.id, trans_type="withdraw", amount=amount)
            return True
        return False
    
    def get_transactions(self, account_number: int):
        account = self.db.query(AccountModel).filter(AccountModel.account_number == account_number).first()
        if not account:
            return None
        transactions = self.db.query(TransactionModel).filter(
            TransactionModel.account_id == account.id
        ).order_by(TransactionModel.timestamp.desc()).all()
        return transactions
    
    def transfer(self, from_account: int, to_account: int, amount: float) -> bool:
        sender = self.db.query(AccountModel).filter(AccountModel.account_number == from_account).first()
        receiver = self.db.query(AccountModel).filter(AccountModel.account_number == to_account).first()

        if not sender or not receiver or sender.available_balance < amount:
            return False

        sender.available_balance -= amount
        sender.total_balance -= amount

        receiver.available_balance += amount
        receiver.total_balance += amount

        now = datetime.utcnow()
        self.db.add(TransactionModel(
            account_id=sender.id,
            amount=-amount,
            type='transfer_out',
            timestamp=now
        ))
        self.db.add(TransactionModel(
            account_id=receiver.id,
            amount=amount,
            type='transfer_in',
            timestamp=now
        ))

        self.db.commit()
        return True
    
    def get_admin_summary(self):
        total_accounts = self.db.query(AccountModel).count()
        total_balance = self.db.query(AccountModel).with_entities(
            func.sum(AccountModel.total_balance)
        ).scalar() or 0.0
        admin_accounts = self.db.query(AccountModel).filter_by(is_admin=True).count()

        return {
            "total_accounts": total_accounts,
            "total_balance": total_balance,
            "admin_accounts": admin_accounts
        }



