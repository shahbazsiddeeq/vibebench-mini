import threading

class Bank:
    def __init__(self, balances: dict):
        if any(balance < 0 for balance in balances.values()):
            raise ValueError("All starting balances must be non-negative.")
        self.balances = balances
        self.locks = {account: threading.Lock() for account in balances}

    def transfer(self, src: str, dst: str, amount: int) -> bool:
        if src == dst:
            raise ValueError("Cannot transfer to the same account.")
        if amount < 0:
            raise ValueError("Transfer amount must be non-negative.")
        if src not in self.balances or dst not in self.balances:
            raise KeyError("One or both accounts are unknown.")

        # Lock accounts in a consistent global order
        first_lock, second_lock = (self.locks[src], self.locks[dst]) if src < dst else (self.locks[dst], self.locks[src])

        with first_lock:
            with second_lock:
                if self.balances[src] < amount:
                    return False
                self.balances[src] -= amount
                self.balances[dst] += amount
                return True

    def balance(self, account: str) -> int:
        if account not in self.balances:
            raise KeyError("Account is unknown.")
        return self.balances[account]

    def total(self) -> int:
        with threading.Lock():  # To ensure total is consistent
            return sum(self.balances.values())
