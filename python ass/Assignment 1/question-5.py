
class Account:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
        self.history = []


class Transaction:
    def __init__(self, account, operation, amount):
        self.account = account
        self.operation = operation
        self.amount = amount


class Bank:
    def deposit(self, account, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")

        account.balance += amount
        account.history.append(Transaction(account.name, "Deposit", amount))

    def withdraw(self, account, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")
        if amount > account.balance:
            raise ValueError("Insufficient balance")

        account.balance -= amount
        account.history.append(Transaction(account.name, "Withdraw", amount))

    def transfer(self, a1, a2, amount):
        self.withdraw(a1, amount)
        self.deposit(a2, amount)

    def batch(self, operations):
        old1 = account1.balance
        old2 = account2.balance
        h1 = len(account1.history)
        h2 = len(account2.history)

        try:
            for op, account, amount in operations:
                if op == "deposit":
                    self.deposit(account, amount)
                elif op == "withdraw":
                    self.withdraw(account, amount)
                else:
                    raise ValueError("Invalid operation")
        except Exception:
            account1.balance = old1
            account2.balance = old2
            del account1.history[h1:]
            del account2.history[h2:]
            print("Batch failed! All changes rolled back.")


# Main program
bank = Bank()

account1 = Account("Amit", 1000)
account2 = Account("Rahul", 500)

bank.deposit(account1, 200)
bank.withdraw(account2, 100)
bank.transfer(account1, account2, 100)

print("Amit Balance:", account1.balance)
print("Rahul Balance:", account2.balance)

# Batch transaction
bank.batch([
    ("deposit", account1, 100),
    ("withdraw", account2, 5000)
])

print("After Batch:")
print("Amit Balance:", account1.balance)
print("Rahul Balance:", account2.balance)
