from abc import ABC, abstractmethod

class Transaction(ABC):
    def __init__(self, account_number, bank_db):
        self.account_number = account_number
        self.bank_db = bank_db
    
    @abstractmethod
    def execute(self):
        pass

class Withdrawal(Transaction):
    def __init__(self, account_number, bank_db, amount):
        super().__init__(account_number, bank_db)
        self.amount = amount
    
    def execute(self):
        if self.bank_db.debit(self.account_number, self.amount):
            return f"Successfully withdrew ${self.amount:.2f}"
        return "Insufficient funds"

class Deposit(Transaction):
    def __init__(self, account_number, bank_db, amount):
        super().__init__(account_number, bank_db)
        self.amount = amount
    
    def execute(self):
        self.bank_db.credit(self.account_number, self.amount)
        return f"Successfully deposited ${self.amount:.2f}"

class BalanceInquiry(Transaction):
    def execute(self):
        available = self.bank_db.get_available_balance(self.account_number)
        total = self.bank_db.get_total_balance(self.account_number)
        return f"Available balance: ${available:.2f}\nTotal balance: ${total:.2f}"