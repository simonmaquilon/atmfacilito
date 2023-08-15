from abc import ABC, abstractmethod

class Transfer_Interface(ABC):
    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def get_balance(self):
        pass

class Account(Transfer_Interface):
    def __init__(self, account_number, balance, owner_name):
        self.__account_number = account_number
        self.__balance = balance
        self.__owner_name = owner_name

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
        else:
            print("Insufficient balance")

    def get_balance(self):
        return self.__balance

class SavingsAccount(Account):
    pass

class CheckingAccount(Account):
    pass

def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@log_decorator
def concurrent_operations(accounts):
    # Perform concurrent operations on accounts using threads or processes
    pass

if __name__ == "__main__":
    account1 = SavingsAccount(12345, 1000, "John")
    account2 = CheckingAccount(67890, 2000, "Jane")

    accounts = [account1, account2]

    concurrent_operations(accounts)
