class EmailNotifier:
    def update(self, account, transaction_type, amount):
        print(f"\n[Email Notification] {transaction_type} of ${amount:.2f} on account {account.account_number}")

class SMSNotifier:
    def update(self, account, transaction_type, amount):
        print(f"\n[SMS Notification] {transaction_type} of ${amount:.2f} on account {account.account_number}")