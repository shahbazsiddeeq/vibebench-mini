import threading
from collections import defaultdict

class Bank:
    def __init__(self, balances):
        if any(balance < 0 for balance in balances.values()):
            raise ValueError("Initial balances cannot be negative.")
        
        self._balances = balances
        self._locks = {account: threading.Lock() for account in balances}
        self._global_lock = threading.Lock()

    def transfer(self, src, dst, amount):
        if amount < 0:
            raise ValueError("Transfer amount cannot be negative.")
        if src == dst:
            raise ValueError("Source and destination accounts must be different.")
        
        with self._global_lock:
            if src not in self._balances or dst not in self._balances:
                raise KeyError("One or both accounts do not exist.")
            
            # Lock accounts in a consistent order to prevent deadlocks
            first, second = sorted([src, dst])
            with self._locks[first], self._locks[second]:
                if self._balances[src] < amount:
                    return False
                self._balances[src] -= amount
                self._balances[dst] += amount
                return True

    def balance(self, account):
        with self._global_lock:
            if account not in self._balances:
                raise KeyError("Account does not exist.")
            return self._balances[account]

    def total(self):
        with self._global_lock:
            return sum(self._balances.values())
