from bank_database import BankDatabase
from account import Account

class AdminInterface:
    def __init__(self, bank_db):
        self.bank_db = bank_db

    def show_menu(self):
        while True:
            print("\nAdmin Menu:")
            print("1 - List all accounts")
            print("2 - Add new account")
            print("3 - Update account")
            print("4 - Delete account")
            print("5 - Exit to main menu")
            print("6 - Quit ATM entirely")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.list_accounts()
            elif choice == '2':
                self.add_account()
            elif choice == '3':
                self.update_account()
            elif choice == '4':
                self.delete_account()
            elif choice == '5':
                break
            elif choice == '6':
                print("\nATM system shutting down. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")

    def list_accounts(self):
        accounts = self.bank_db.get_all_accounts()
        print("\nAll Accounts:")
        print("-" * 60)
        print(f"{'Account #':<12} {'PIN':<8} {'Available':<12} {'Total':<12} {'Admin'}")
        print("-" * 60)
        for acc in accounts:
            print(f"{acc['account_number']:<12} {acc['pin']:<8} "
                  f"${acc['available_balance']:<10.2f} ${acc['total_balance']:<10.2f} "
                  f"{'Yes' if acc['is_admin'] else 'No'}")
        print("-" * 60)

    def add_account(self):
        print("\nAdd New Account:")
        try:
            acc_num = int(input("Account number: "))
            pin = int(input("PIN: "))
            avail_bal = float(input("Available balance: "))
            total_bal = float(input("Total balance: "))
            is_admin = input("Is admin? (y/n): ").lower() == 'y'

            new_account = Account(acc_num, pin, avail_bal, total_bal, is_admin)
            if self.bank_db.add_account(new_account):
                print("Account added successfully!")
            else:
                print("Account number already exists!")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    def update_account(self):
        print("\nUpdate Account:")
        try:
            acc_num = int(input("Enter account number to update: "))
            account = self.bank_db.get_account(acc_num)
            if not account:
                print("Account not found!")
                return

            print("\nLeave blank to keep current value")
            new_pin = input(f"New PIN (current: {account.pin}): ")
            new_avail = input(f"New available balance (current: {account.available_balance}): ")
            new_total = input(f"New total balance (current: {account.total_balance}): ")
            new_admin = input(f"Admin status [y/n] (current: {'y' if account.is_admin else 'n'}): ")

            update_data = {}
            if new_pin: update_data['pin'] = int(new_pin)
            if new_avail: update_data['available_balance'] = float(new_avail)
            if new_total: update_data['total_balance'] = float(new_total)
            if new_admin: update_data['is_admin'] = new_admin.lower() == 'y'

            if update_data and self.bank_db.update_account(acc_num, update_data):
                print("Account updated successfully!")
            else:
                print("No changes made or update failed.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    def delete_account(self):
        print("\nDelete Account:")
        try:
            acc_num = int(input("Enter account number to delete: "))
            if self.bank_db.delete_account(acc_num):
                print("Account deleted successfully!")
            else:
                print("Account not found or cannot delete admin account!")
        except ValueError:
            print("Invalid account number. Please enter a valid number.")