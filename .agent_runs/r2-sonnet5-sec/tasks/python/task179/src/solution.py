"""
Thread-safe bank account simulation.

This module implements a `Bank` class that manages a set of named accounts
with integer balances. All operations are safe for concurrent use from
multiple threads:

* Each account has its own lock so unrelated accounts can be operated on
  independently and concurrently.
* Transfers between two accounts always acquire the two required locks in a
  fixed, globally consistent order (based on account name), regardless of
  the direction of the transfer, which prevents deadlocks.
* No money is ever created or destroyed: total() is invariant across any
  sequence of successful and failed transfers.

Only the Python standard library is used (threading module for
synchronization). No external input is executed or evaluated.
"""

import threading
from typing import Dict, Hashable


class Bank:
    """A simple thread-safe bank with per-account locking."""

    __slots__ = ("_balances", "_locks", "_total_lock")

    def __init__(self, balances: Dict[Hashable, int]) -> None:
        if not isinstance(balances, dict):
            raise TypeError("balances must be a dict")

        validated: Dict[Hashable, int] = {}
        for account, bal in balances.items():
            if not isinstance(bal, int) or isinstance(bal, bool):
                raise ValueError("balances must be integers")
            if bal < 0:
                raise ValueError("starting balances must be non-negative")
            validated[account] = bal

        # Store balances and a dedicated lock per account.
        self._balances: Dict[Hashable, int] = dict(validated)
        self._locks: Dict[Hashable, threading.Lock] = {
            account: threading.Lock() for account in validated
        }
        # Guards structural/global reads such as total(), not strictly
        # required for correctness of per-account locking but keeps total()
        # consistent with respect to concurrent transfers.
        self._total_lock = threading.Lock()

    def _lock_order(self, a: Hashable, b: Hashable):
        """Return the two accounts' locks in a fixed global order.

        The order is derived from a stable, total ordering of account keys
        (their string representation) so that any two threads attempting to
        lock the same pair of accounts -- regardless of transfer direction --
        always acquire the locks in the same sequence, preventing deadlock.
        """
        key_a = repr(a)
        key_b = repr(b)
        if key_a <= key_b:
            return self._locks[a], self._locks[b]
        return self._locks[b], self._locks[a]

    def transfer(self, src: Hashable, dst: Hashable, amount: int) -> bool:
        """Atomically transfer `amount` units from `src` to `dst`.

        Raises:
            KeyError: if either account is unknown.
            ValueError: if amount is negative or src == dst.

        Returns:
            True if the transfer succeeded (src had sufficient funds),
            False if src had insufficient funds (balances unchanged).
        """
        if src not in self._balances or dst not in self._balances:
            # Raise a KeyError referencing the missing account without
            # leaking internal state.
            missing = src if src not in self._balances else dst
            raise KeyError(missing)

        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("amount must be an integer")
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if src == dst:
            raise ValueError("src and dst must be different accounts")

        first_lock, second_lock = self._lock_order(src, dst)

        with first_lock, second_lock:
            if self._balances[src] < amount:
                return False
            self._balances[src] -= amount
            self._balances[dst] += amount
            return True

    def balance(self, account: Hashable) -> int:
        """Return the current balance of `account`.

        Raises:
            KeyError: if the account is unknown.
        """
        if account not in self._balances:
            raise KeyError(account)
        with self._locks[account]:
            return self._balances[account]

    def total(self) -> int:
        """Return the sum of all account balances.

        This value is invariant under any sequence of successful or failed
        transfers, since transfers only move funds between existing
        accounts and never fabricate or destroy money.
        """
        # Acquire all account locks (in a fixed, stable order) to obtain a
        # consistent snapshot of the balances.
        accounts = sorted(self._balances.keys(), key=repr)
        acquired = []
        try:
            for account in accounts:
                lock = self._locks[account]
                lock.acquire()
                acquired.append(lock)
            return sum(self._balances.values())
        finally:
            for lock in reversed(acquired):
                lock.release()
