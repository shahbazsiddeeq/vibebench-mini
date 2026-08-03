"""
A thread-safe bank account module.

Provides a Bank class supporting atomic, deadlock-free transfers between
accounts using per-account locks acquired in a fixed global order.
"""

import threading


class Bank:
    def __init__(self, balances: dict):
        for name, bal in balances.items():
            if bal < 0:
                raise ValueError(f"Starting balance for {name!r} is negative")

        self._balances = dict(balances)
        self._locks = {name: threading.Lock() for name in balances}
        # Global lock protects the structure itself (not needed for balance
        # updates since those are protected by per-account locks, but used
        # for total() consistency and safe dict access).
        self._global_lock = threading.Lock()

    def _get_lock(self, account):
        try:
            return self._locks[account]
        except KeyError:
            raise KeyError(account)

    def transfer(self, src, dst, amount: int) -> bool:
        if src not in self._balances:
            raise KeyError(src)
        if dst not in self._balances:
            raise KeyError(dst)
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if src == dst:
            raise ValueError("src and dst must differ")

        lock_src = self._locks[src]
        lock_dst = self._locks[dst]

        # Acquire locks in a fixed global order (based on account name)
        # regardless of transfer direction, to avoid deadlocks.
        if src < dst:
            first, second = lock_src, lock_dst
        else:
            first, second = lock_dst, lock_src

        with first:
            with second:
                if self._balances[src] < amount:
                    return False
                self._balances[src] -= amount
                self._balances[dst] += amount
                return True

    def balance(self, account) -> int:
        if account not in self._balances:
            raise KeyError(account)
        with self._locks[account]:
            return self._balances[account]

    def total(self) -> int:
        # Acquire all locks in a fixed global order to get a consistent
        # snapshot of the total balance.
        names = sorted(self._balances.keys())
        acquired = []
        try:
            for name in names:
                lock = self._locks[name]
                lock.acquire()
                acquired.append(lock)
            return sum(self._balances[name] for name in names)
        finally:
            for lock in reversed(acquired):
                lock.release()
