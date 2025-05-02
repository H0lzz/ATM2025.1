from abc import ABC, abstractmethod

class CashDispenserStrategy(ABC):
    @abstractmethod
    def dispense(self, amount):
        pass

class StandardDispenser(CashDispenserStrategy):
    def dispense(self, amount):
        print(f"\nDispensing ${amount:.2f} in $20 bills")

class LargeBillDispenser(CashDispenserStrategy):
    def dispense(self, amount):
        print(f"\nDispensing ${amount:.2f} in $100 bills")