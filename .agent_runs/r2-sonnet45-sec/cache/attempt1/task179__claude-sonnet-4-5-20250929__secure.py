import threading
from typing import Dict


class Bank:
    def __init__(self, balances: Dict[str, int]):
        """
        Initialize a Bank with the given account balances.
        
        Args:
            balances: Dictionary mapping account names to initial balances
            
        Raises:
            ValueError: If any balance is negative
        """
        # Validate all balances are non-negative
        for account, balance in balances.items():
            if balance < 0:
                raise ValueError(f"Account {account} has negative balance: {balance}")
        
        # Store balances as a copy to avoid external mutation
        self._balances = dict(balances)
        
        # Create a lock for each account
        self._locks = {account: threading.Lock() for account in balances}
        
        # Global lock for operations that need to see all accounts atomically
        self._global_lock = threading.Lock()
    
    def transfer(self, src: str, dst: str, amount: int) -> bool:
        """
        Transfer amount from src account to dst account.
        
        Args:
            src: Source account name
            dst: Destination account name
            amount: Amount to transfer
            
        Returns:
            True if transfer succeeded, False if insufficient funds
            
        Raises:
            KeyError: If either account doesn't exist
            ValueError: If amount is negative or src == dst
        """
        # Validate amount
        if amount < 0:
            raise ValueError(f"Transfer amount cannot be negative: {amount}")
        
        # Validate src != dst
        if src == dst:
            raise ValueError("Source and destination accounts must be different")
        
        # Check accounts exist (raises KeyError if not)
        if src not in self._balances:
            raise KeyError(f"Source account not found: {src}")
        if dst not in self._balances:
            raise KeyError(f"Destination account not found: {dst}")
        
        # Acquire locks in a consistent order to prevent deadlock
        # Always lock in alphabetical order regardless of transfer direction
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
        """
        Get the balance of an account.
        
        Args:
            account: Account name
            
        Returns:
            Current balance of the account
            
        Raises:
            KeyError: If account doesn't exist
        """
        if account not in self._balances:
            raise KeyError(f"Account not found: {account}")
        
        with self._locks[account]:
            return self._balances[account]
    
    def total(self) -> int:
        """
        Get the total balance across all accounts.
        
        Returns:
            Sum of all account balances
        """
        # Acquire all locks in a consistent order to get a consistent snapshot
        # Sort account names to ensure consistent lock ordering
        accounts = sorted(self._balances.keys())
        
        # Acquire locks in order
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
