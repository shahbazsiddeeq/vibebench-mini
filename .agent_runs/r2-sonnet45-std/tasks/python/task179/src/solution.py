import threading
from typing import Dict


class Bank:
    def __init__(self, balances: Dict[str, int]):
        # Validate that no balance is negative
        for account, balance in balances.items():
            if balance < 0:
                raise ValueError(f"Account {account} has negative balance: {balance}")
        
        # Store balances
        self._balances = dict(balances)
        
        # Create a lock for each account
        self._locks = {account: threading.Lock() for account in balances}
        
        # Global lock for operations that need to see consistent state across all accounts
        self._global_lock = threading.Lock()
    
    def transfer(self, src: str, dst: str, amount: int) -> bool:
        # Validate amount
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        
        # Validate src != dst
        if src == dst:
            raise ValueError("Source and destination accounts must be different")
        
        # Check that both accounts exist (raises KeyError if not)
        if src not in self._balances:
            raise KeyError(f"Source account {src} not found")
        if dst not in self._balances:
            raise KeyError(f"Destination account {dst} not found")
        
        # Acquire locks in a consistent order to prevent deadlock
        # Always lock in alphabetical order
        first, second = (src, dst) if src < dst else (dst, src)
        
        with self._locks[first]:
            with self._locks[second]:
                # Check if source has sufficient funds
                if self._balances[src] < amount:
                    return False
                
                # Perform the transfer
                self._balances[src] -= amount
                self._balances[dst] += amount
                return True
    
    def balance(self, account: str) -> int:
        # Check that account exists
        if account not in self._balances:
            raise KeyError(f"Account {account} not found")
        
        # Read balance with lock held
        with self._locks[account]:
            return self._balances[account]
    
    def total(self) -> int:
        # To get a consistent snapshot of all balances, we need to lock all accounts
        # Lock them in a consistent order (alphabetically)
        accounts = sorted(self._balances.keys())
        
        # Acquire all locks in order
        locks_held = []
        try:
            for account in accounts:
                self._locks[account].acquire()
                locks_held.append(account)
            
            # Now we have all locks, compute total
            return sum(self._balances.values())
        finally:
            # Release all locks in reverse order
            for account in reversed(locks_held):
                self._locks[account].release()
