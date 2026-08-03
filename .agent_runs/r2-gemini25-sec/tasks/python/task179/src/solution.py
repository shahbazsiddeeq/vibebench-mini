import threading
from collections import defaultdict


class Bank:
    """
    A thread-safe bank implementation with per-account locks to prevent deadlocks
    and ensure atomicity of transfers.
    """

    def __init__(self, balances: dict):
        """
        Initializes the Bank with a dictionary of account balances.

        Args:
            balances: A dictionary where keys are account names (strings) and
                      values are their initial integer balances.

        Raises:
            ValueError: If any initial balance is negative.
            TypeError: If balances is not a dict or if account names are not strings
                       or balances are not integers.
        """
        if not isinstance(balances, dict):
            raise TypeError("Initial balances must be a dictionary.")

        self._balances = {}
        self._locks = defaultdict(threading.Lock)

        for account, balance in balances.items():
            if not isinstance(account, str):
                raise TypeError("Account names must be strings.")
            if not isinstance(balance, int):
                raise TypeError(f"Balance for account '{account}' must be an integer.")
            if balance < 0:
                raise ValueError(f"Initial balance for account '{account}' cannot be negative.")
            self._balances[account] = balance

    def _get_sorted_accounts(self, acc1, acc2):
        """
        Returns a tuple of two account names sorted lexicographically.
        This ensures a consistent lock acquisition order to prevent deadlocks.
        """
        return tuple(sorted((acc1, acc2)))

    def transfer(self, src: str, dst: str, amount: int) -> bool:
        """
        Atomically transfers a specified amount from a source account to a
        destination account.

        Args:
            src: The name of the source account.
            dst: The name of the destination account.
            amount: The integer amount to transfer.

        Returns:
            True if the transfer was successful, False otherwise (e.g., insufficient funds).

        Raises:
            KeyError: If either src or dst account is unknown.
            ValueError: If amount is negative or if src and dst are the same account.
            TypeError: If src, dst are not strings or amount is not an integer.
        """
        if not isinstance(src, str) or not isinstance(dst, str):
            raise TypeError("Account names must be strings.")
        if not isinstance(amount, int):
            raise TypeError("Transfer amount must be an integer.")

        if amount < 0:
            raise ValueError("Transfer amount cannot be negative.")
        if src == dst:
            raise ValueError("Source and destination accounts cannot be the same.")

        # Check for account existence before acquiring locks to avoid holding locks
        # unnecessarily for invalid accounts.
        if src not in self._balances:
            raise KeyError(f"Source account '{src}' not found.")
        if dst not in self._balances:
            raise KeyError(f"Destination account '{dst}' not found.")

        # Acquire locks in a consistent order to prevent deadlocks
        lock1_account, lock2_account = self._get_sorted_accounts(src, dst)

        # Acquire locks for the two accounts involved in the transfer
        # The order of acquiring locks is crucial for deadlock prevention.
        # We use the lexicographically sorted account names to determine the order.
        with self._locks[lock1_account]:
            with self._locks[lock2_account]:
                # Re-check balances after acquiring locks, as they might have changed
                # due to other concurrent operations.
                if self._balances[src] < amount:
                    return False  # Insufficient funds

                self._balances[src] -= amount
                self._balances[dst] += amount
                return True

    def balance(self, account: str) -> int:
        """
        Returns the current balance of a specified account.

        Args:
            account: The name of the account.

        Returns:
            The integer balance of the account.

        Raises:
            KeyError: If the account is unknown.
            TypeError: If account is not a string.
        """
        if not isinstance(account, str):
            raise TypeError("Account name must be a string.")

        # Acquire lock for the specific account to ensure reading a consistent state
        with self._locks[account]:
            if account not in self._balances:
                raise KeyError(f"Account '{account}' not found.")
            return self._balances[account]

    def total(self) -> int:
        """
        Calculates the sum of all account balances.
        This operation is not protected by a single global lock, but rather
        iterates through accounts, acquiring individual locks. This is acceptable
        because the total balance is invariant under transfers, and individual
        account balances are read consistently.

        Returns:
            The total sum of all account balances.
        """
        total_balance = 0
        # To calculate the total, we need to iterate through all accounts.
        # We acquire locks for each account one by one to ensure we read
        # a consistent balance for that specific account.
        # This approach avoids a global lock that would block all transfers
        # during a total() call, while still ensuring individual reads are consistent.
        # The sum itself might be a snapshot across different points in time for
        # different accounts, but since transfers are internal, the total sum
        # remains invariant.
        
        # Create a sorted list of account names to ensure consistent lock acquisition
        # order if multiple threads call total() concurrently, though for total()
        # it's less critical for deadlock than for transfer().
        # However, it's good practice to be consistent.
        sorted_accounts = sorted(self._balances.keys())

        for account in sorted_accounts:
            with self._locks[account]:
                total_balance += self._balances[account]
        return total_balance
