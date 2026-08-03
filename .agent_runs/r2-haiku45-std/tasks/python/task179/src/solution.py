import threading
from typing import Dict


class Bank:
    def __init__(self, balances: Dict[str, int]):
        """Initialize bank with account balances.
        
        Args:
            balances: Dictionary mapping account names to integer balances.
            
        Raises:
            ValueError: If any balance is negative.
        """
        for account, balance in balances.items():
            if balance < 0:
                raise ValueError(f"Negative balance for account {account}")
        
        self._balances = dict(balances)
        self._locks = {account: threading.Lock() for account in balances}
        self._global_lock = threading.Lock()
    
    def transfer(self, src: str, dst: str, amount: int) -> bool:
        """Transfer amount from src account to dst account.
        
        Args:
            src: Source account name.
            dst: Destination account name.
            amount: Amount to transfer.
            
        Returns:
            True if transfer succeeded, False if src has insufficient funds.
            
        Raises:
            KeyError: If either account doesn't exist.
            ValueError: If amount < 0 or src == dst.
        """
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        
        if src == dst:
            raise ValueError("Source and destination cannot be the same")
        
        # Check that both accounts exist
        if src not in self._balances:
            raise KeyError(f"Account {src} not found")
        if dst not in self._balances:
            raise KeyError(f"Account {dst} not found")
        
        # Acquire locks in a fixed global order to prevent deadlock
        # Sort account names to ensure consistent lock ordering
        accounts = sorted([src, dst])
        lock1 = self._locks[accounts[0]]
        lock2 = self._locks[accounts[1]]
        
        with lock1:
            with lock2:
                # Check if source has sufficient funds
                if self._balances[src] < amount:
                    return False
                
                # Perform the transfer
                self._balances[src] -= amount
                self._balances[dst] += amount
                return True
    
    def balance(self, account: str) -> int:
        """Get the balance of an account.
        
        Args:
            account: Account name.
            
        Returns:
            The balance of the account.
            
        Raises:
            KeyError: If account doesn't exist.
        """
        if account not in self._balances:
            raise KeyError(f"Account {account} not found")
        
        with self._locks[account]:
            return self._balances[account]
    
    def total(self) -> int:
        """Get the total balance across all accounts.
        
        Returns:
            Sum of all account balances.
        """
        # Acquire all locks in sorted order to prevent deadlock
        accounts = sorted(self._balances.keys())
        locks = [self._locks[account] for account in accounts]
        
        # Acquire all locks
        for lock in locks:
            lock.acquire()
        
        try:
            return sum(self._balances.values())
        finally:
            # Release all locks in reverse order
            for lock in reversed(locks):
                lock.release()
