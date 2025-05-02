from bank_database import BankDatabase
from admin import AdminInterface

class ATM:
    def __init__(self):
        self.current_account_number = None
        self.bank_database = BankDatabase()
        self.admin_interface = AdminInterface(self.bank_database)
        self.display_welcome_message()

    def display_welcome_message(self):
        print("\nWelcome to the ATM!")
        self.prompt_for_account_number()

    def prompt_for_account_number(self):
        print("\nPlease enter your account number: ", end="")
        account_number = int(input())
        print("Enter your PIN: ", end="")
        pin = int(input())

        if self.bank_database.authenticate_user(account_number, pin):
            self.current_account_number = account_number
            if self.bank_database.is_admin(account_number):
                self.admin_interface.show_menu()
                self.current_account_number = None
                self.display_welcome_message()
            else:
                self.display_main_menu()
        else:
            print("Invalid account number or PIN. Please try again.")
            self.prompt_for_account_number()

    def display_main_menu(self):
        print("\nMain menu:")
        print("1 - View my balance")
        print("2 - Withdraw cash")
        print("3 - Deposit funds")
        print("4 - Exit")
        print("Enter a choice: ", end="")
        choice = int(input())

        if choice == 1:
            self.display_balance()
        elif choice == 2:
            self.withdraw()
        elif choice == 3:
            self.deposit()
        elif choice == 4:
            print("\nThank you! Goodbye!")
            self.current_account_number = None
            self.display_welcome_message()
        else:
            print("\nInvalid choice. Please try again.")
            self.display_main_menu()

    def display_balance(self):
        available_balance = self.bank_database.get_available_balance(self.current_account_number)
        total_balance = self.bank_database.get_total_balance(self.current_account_number)

        print("\nBalance Information:")
        print(f" - Available balance: ${available_balance:.2f}")
        print(f" - Total balance: ${total_balance:.2f}")
        self.display_main_menu()

    def withdraw(self):
        print("\nWithdrawal options:")
        print("1 - $20")
        print("2 - $40")
        print("3 - $60")
        print("4 - $100")
        print("5 - $200")
        print("6 - Cancel transaction")
        print("Choose a withdrawal amount: ", end="")
        choice = int(input())

        amounts = {1: 20, 2: 40, 3: 60, 4: 100, 5: 200}
        
        if choice in amounts:
            amount = amounts[choice]
            available_balance = self.bank_database.get_available_balance(self.current_account_number)
            
            if amount <= available_balance:
                self.bank_database.debit(self.current_account_number, amount)
                print("\nPlease take your cash from the cash dispenser.")
                print(f"Your new available balance is: ${available_balance - amount:.2f}")
            else:
                print("\nInsufficient funds in your account.")
        elif choice == 6:
            print("\nCanceling transaction...")
        else:
            print("\nInvalid choice. Transaction canceled.")
        
        self.display_main_menu()

    def deposit(self):
        print("\nPlease enter a deposit amount in CENTS (or 0 to cancel): ", end="")
        amount = int(input()) / 100
        
        if amount > 0:
            print("\nPlease insert a deposit envelope containing")
            print(f"${amount:.2f} in the deposit slot.")
            print("\nYour envelope has been received.")
            print("NOTE: The money deposited will not be available until we")
            print("verify the amount of any enclosed cash, and any enclosed checks clear.")
            
            self.bank_database.credit(self.current_account_number, amount)
            available_balance = self.bank_database.get_available_balance(self.current_account_number)
            total_balance = self.bank_database.get_total_balance(self.current_account_number)
            
            print(f"\nYour new available balance is: ${available_balance:.2f}")
            print(f"Your new total balance is: ${total_balance:.2f}")
        else:
            print("\nCanceling transaction...")
        
        self.display_main_menu()