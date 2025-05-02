from abc import ABC, abstractmethod

class AuthHandler(ABC):
    def __init__(self, successor=None):
        self._successor = successor
    
    @abstractmethod
    def handle(self, account_number, pin, bank_db):
        pass

class PinAuthHandler(AuthHandler):
    def handle(self, account_number, pin, bank_db):
        account = bank_db.get_account(account_number)
        if account and account.validate_pin(pin):
            return True
        elif self._successor:
            return self._successor.handle(account_number, pin, bank_db)
        return False

class BiometricAuthHandler(AuthHandler):
    def handle(self, account_number, pin, bank_db):
        # Simulated biometric check - in real system would use actual biometric verification
        if account_number == 99999:  # Admin bypass for demo
            return True
        elif self._successor:
            return self._successor.handle(account_number, pin, bank_db)
        return False