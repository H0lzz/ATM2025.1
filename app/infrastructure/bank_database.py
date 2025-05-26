import json
from domain.account import Account

class BankDatabase:
    def __init__(self, filename='accounts.json'):
        self.filename = filename
        self.accounts = self._load_accounts()

    def _load_accounts(self):
        try:
            with open(self.filename, 'r') as file:
                accounts_data = json.load(file)
                return [Account.from_dict(acc) for acc in accounts_data]
        except (FileNotFoundError, json.JSONDecodeError):

            default_accounts = [
                Account(12345, 54321, 1000.0, 1200.0).to_dict(),
                Account(98765, 56789, 200.0, 200.0).to_dict(),
                Account(99999, 99999, 0, 0, True).to_dict()
            ]
            with open(self.filename, 'w') as file:
                json.dump(default_accounts, file, indent=2)
            return [Account.from_dict(acc) for acc in default_accounts]

    def _save_accounts(self):
        with open(self.filename, 'w') as file:
            accounts_data = [acc.to_dict() for acc in self.accounts]
            json.dump(accounts_data, file, indent=2)

    def get_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def authenticate_user(self, account_number, pin):
        account = self.get_account(account_number)
        if account is not None:
            return account.validate_pin(pin)
        return False

    def is_admin(self, account_number):
        account = self.get_account(account_number)
        return account.is_admin if account else False

    def add_account(self, account):
        if not self.get_account(account.account_number):
            self.accounts.append(account)
            self._save_accounts()
            return True
        return False

    def delete_account(self, account_number):
        account = self.get_account(account_number)
        if account and not account.is_admin:
            self.accounts.remove(account)
            self._save_accounts()
            return True
        return False

    def update_account(self, account_number, new_data):
        account = self.get_account(account_number)
        if account:
            for key, value in new_data.items():
                if hasattr(account, key) and key != 'account_number':
                    setattr(account, key, value)
            self._save_accounts()
            return True
        return False

    def get_all_accounts(self):
        return [acc.to_dict() for acc in self.accounts]
    
    def get_available_balance(self, account_number):
        account = self.get_account(account_number)
        return account.get_available_balance()

    def get_total_balance(self, account_number):
        account = self.get_account(account_number)
        return account.get_total_balance()

    def credit(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            account.credit(amount)
            self._save_accounts()
            return True
        return False

    def debit(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            success = account.debit(amount)
            if success:
                self._save_accounts()
                return True
        return False