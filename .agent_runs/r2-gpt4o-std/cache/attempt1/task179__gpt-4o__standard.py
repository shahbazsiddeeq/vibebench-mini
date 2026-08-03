import threading

class Bank:
    def __init__(self, balances):
        if any(balance < 0 for balance in balances.values()):
            raise ValueError("Initial balances cannot be negative.")
        
        self.balances = balances
        self.locks = {account: threading.Lock() for account in balances}
        self.global_lock = threading.Lock()

    def transfer(self, src, dst, amount):
        if amount < 0:
            raise ValueError("Transfer amount cannot be negative.")
        if src == dst:
            raise ValueError("Source and destination accounts must be different.")
        if src not in self.balances or dst not in self.balances:
            raise KeyError("Account not found.")

        # Lock accounts in a consistent order to prevent deadlocks
        first, second = (src, dst) if src < dst else (dst, src)

        with self.locks[first], self.locks[second]:
            if self.balances[src] < amount:
                return False
            self.balances[src] -= amount
            self.balances[dst] += amount
            return True

    def balance(self, account):
        if account not in self.balances:
            raise KeyError("Account not found.")
        with self.locks[account]:
            return self.balances[account]

    def total(self):
        with self.global_lock:
            return sum(self.balances.values())
