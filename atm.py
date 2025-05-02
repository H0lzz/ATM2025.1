from bank_database import BankDatabase
from admin import AdminInterface
from transaction import Withdrawal, Deposit, BalanceInquiry
from cash_dispenser import StandardDispenser, LargeBillDispenser
from auth_handler import PinAuthHandler, BiometricAuthHandler
from observers import EmailNotifier, SMSNotifier
from account_factory import AccountFactory

class ATM:
    def __init__(self):
        self.current_account_number = None
        self.bank_db = BankDatabase()
        self.admin_interface = AdminInterface(self.bank_db)
        self.setup_components()
        self.display_welcome_message()

    def setup_components(self):
        self.cash_dispenser = StandardDispenser()
        
        self.auth_handler = BiometricAuthHandler(PinAuthHandler())
        
        self.email_notifier = EmailNotifier()
        self.sms_notifier = SMSNotifier()
        self.attach_observers_to_existing_accounts()

    def attach_observers_to_existing_accounts(self):
        for account in self.bank_db.accounts:
            account.attach(self.email_notifier)
            account.attach(self.sms_notifier)

    def display_welcome_message(self):
        print("\nWelcome to the ATM!")
        self.prompt_for_account_number()

    def prompt_for_account_number(self):
        print("\nPlease enter your account number: ", end="")
        account_number = int(input())
        print("Enter your PIN: ", end="")
        pin = int(input())

        if self.authenticate_user(account_number, pin):
            self.current_account_number = account_number
            if self.bank_db.is_admin(account_number):
                self.admin_interface.show_menu()
                self.current_account_number = None
                self.display_welcome_message()
            else:
                self.display_main_menu()
        else:
            print("Invalid account number or PIN. Please try again.")
            self.prompt_for_account_number()

    def authenticate_user(self, account_number, pin):
        return self.auth_handler.handle(account_number, pin, self.bank_db)

    def display_main_menu(self):
        while True:
            print("\nMain menu:")
            print("1 - View my balance")
            print("2 - Withdraw cash")
            print("3 - Deposit funds")
            print("4 - Change cash dispenser mode")
            print("5 - Exit ATM")
            choice = input("Enter a choice: ")

            if choice == '1':
                self.display_balance()
            elif choice == '2':
                self.withdraw()
            elif choice == '3':
                self.deposit()
            elif choice == '4':
                self.change_dispenser_mode()
            elif choice == '5':
                print("\nThank you for using our ATM. Goodbye!")
                exit()  # Terminate the program
            else:
                print("Invalid choice. Please try again.")

    def display_balance(self):
        transaction = BalanceInquiry(self.current_account_number, self.bank_db)
        result = transaction.execute()
        print("\nBalance Information:")
        print(result)
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
            transaction = Withdrawal(self.current_account_number, self.bank_db, amount)
            result = transaction.execute()
            print(f"\n{result}")
            
            if "Withdrew" in result:
                self.cash_dispenser.dispense(amount)
        elif choice == 6:
            print("\nCanceling transaction...")
        else:
            print("\nInvalid choice. Transaction canceled.")
        
        self.display_main_menu()

    def deposit(self):
        print("\nPlease enter a deposit amount in CENTS (or 0 to cancel): ", end="")
        amount = int(input()) / 100
        
        if amount > 0:
            transaction = Deposit(self.current_account_number, self.bank_db, amount)
            result = transaction.execute()
            
            print("\nPlease insert a deposit envelope containing")
            print(f"${amount:.2f} in the deposit slot.")
            print("\nYour envelope has been received.")
            print("NOTE: The money deposited will not be available until we")
            print("verify the amount of any enclosed cash, and any enclosed checks clear.")
            
            print(f"\n{result}")
        else:
            print("\nCanceling transaction...")
        
        self.display_main_menu()

    def change_dispenser_mode(self):
        print("\nSelect cash dispenser mode:")
        print("1 - Standard ($20 bills)")
        print("2 - Large bills ($100 bills)")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            self.cash_dispenser = StandardDispenser()
            print("Cash dispenser set to standard mode")
        elif choice == '2':
            self.cash_dispenser = LargeBillDispenser()
            print("Cash dispenser set to large bill mode")
        else:
            print("Invalid choice")
        
        self.display_main_menu()