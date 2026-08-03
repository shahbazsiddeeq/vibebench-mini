import threading

class Bank:
    def __init__(self, balances: dict):
        self._balances = {}
        self._locks = {}
        self._account_names = []

        for account, balance in balances.items():
            if not isinstance(balance, int) or balance < 0:
                raise ValueError("Initial balances must be non-negative integers.")
            self._balances[account] = balance
            self._locks[account] = threading.Lock()
            self._account_names.append(account)
        
        # Sort account names to establish a global order for locking
        self._account_names.sort()

    def _get_account_lock_order(self, account1, account2):
        """
        Determines the global order for acquiring locks for two accounts.
        This prevents deadlocks by ensuring locks are always acquired in the same order.
        """
        idx1 = self._account_names.index(account1)
        idx2 = self._account_names.index(account2)

        if idx1 < idx2:
            return account1, account2
        else:
            return account2, account1

    def transfer(self, src, dst, amount) -> bool:
        if src == dst:
            raise ValueError("Source and destination accounts cannot be the same.")
        if amount < 0:
            raise ValueError("Transfer amount cannot be negative.")

        if src not in self._balances:
            raise KeyError(f"Source account '{src}' not found.")
        if dst not in self._balances:
            raise KeyError(f"Destination account '{dst}' not found.")

        # Acquire locks in a fixed global order to prevent deadlocks
        first_lock_account, second_lock_account = self._get_account_lock_order(src, dst)

        with self._locks[first_lock_account]:
            with self._locks[second_lock_account]:
                # Re-check balances after acquiring locks, as they might have changed
                if self._balances[src] < amount:
                    return False
                
                self._balances[src] -= amount
                self._balances[dst] += amount
                return True

    def balance(self, account) -> int:
        if account not in self._balances:
            raise KeyError(f"Account '{account}' not found.")
        
        # Acquire lock to ensure reading a consistent balance
        with self._locks[account]:
            return self._balances[account]

    def total(self) -> int:
        total_sum = 0
        # Acquire all locks in global order to ensure a consistent sum
        # This is a coarse-grained lock for total(), but necessary for correctness
        # if balances can change concurrently.
        # For a truly concurrent total, one might use a global read-write lock
        # or atomic operations if available, but given the constraints,
        # acquiring all individual locks is the safest approach.
        
        # Create a list of locks to acquire in order
        locks_to_acquire = [self._locks[name] for name in self._account_names]

        # Acquire all locks
        for lock in locks_to_acquire:
            lock.acquire()
        
        try:
            for balance in self._balances.values():
                total_sum += balance
        finally:
            # Release all locks
            for lock in reversed(locks_to_acquire): # Release in reverse order of acquisition
                lock.release()
        
        return total_sum
