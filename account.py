class Account:
    def __init__(self, account_number, pin, available_balance=0, total_balance=0, is_admin=False):
        self.account_number = account_number
        self.pin = pin
        self.available_balance = available_balance
        self.total_balance = total_balance
        self.is_admin = is_admin

    def validate_pin(self, user_pin):
        return user_pin == self.pin

    def get_available_balance(self):
        return self.available_balance

    def get_total_balance(self):
        return self.total_balance

    def credit(self, amount):
        self.total_balance += amount
        self.available_balance += amount

    def debit(self, amount):
        if amount <= self.available_balance:
            self.available_balance -= amount
            self.total_balance -= amount
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