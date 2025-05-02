from abc import ABC, abstractmethod

class AccountObserver(ABC):
    @abstractmethod
    def update(self, account, transaction_type, amount):
        pass

class Account:
    def __init__(self, account_number, pin, available_balance=0, total_balance=0, is_admin=False):
        self.account_number = account_number
        self.pin = pin
        self.available_balance = available_balance
        self.total_balance = total_balance
        self.is_admin = is_admin
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify_observers(self, transaction_type, amount):
        for observer in self._observers:
            observer.update(self, transaction_type, amount)

    def validate_pin(self, user_pin):
        return user_pin == self.pin

    def get_available_balance(self):
        return self.available_balance

    def get_total_balance(self):
        return self.total_balance

    def credit(self, amount):
        self.total_balance += amount
        self.available_balance += amount
        self.notify_observers("Deposit", amount)

    def debit(self, amount):
        if amount <= self.available_balance:
            self.available_balance -= amount
            self.total_balance -= amount
            self.notify_observers("Withdrawal", amount)
            return True
        return False

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'pin': self.pin,
            'available_balance': self.available_balance,
            'total_balance': self.total_balance,
            'is_admin': self.is_admin
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['account_number'],
            data['pin'],
            data['available_balance'],
            data['total_balance'],
            data.get('is_admin', False)
        )

class SavingsAccount(Account):
    def __init__(self, account_number, pin, available_balance=0, total_balance=0, interest_rate=0.01):
        super().__init__(account_number, pin, available_balance, total_balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.total_balance * self.interest_rate
        self.credit(interest)
        return interest

class CheckingAccount(Account):
    def __init__(self, account_number, pin, available_balance=0, total_balance=0, monthly_fee=5.00):
        super().__init__(account_number, pin, available_balance, total_balance)
        self.monthly_fee = monthly_fee

    def apply_monthly_fee(self):
        return self.debit(self.monthly_fee)