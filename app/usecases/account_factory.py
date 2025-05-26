from domain.account import Account, SavingsAccount, CheckingAccount

class AccountFactory:
    @staticmethod
    def create_account(account_type, account_number, pin, available_balance=0, total_balance=0, is_admin=False):
        if account_type == "savings":
            return SavingsAccount(account_number, pin, available_balance, total_balance)
        elif account_type == "checking":
            return CheckingAccount(account_number, pin, available_balance, total_balance)
        else:
            return Account(account_number, pin, available_balance, total_balance, is_admin)