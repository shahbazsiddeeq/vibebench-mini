"""Thread-safe, deadlock-free bank account transfers."""

from __future__ import annotations

import threading
from contextlib import ExitStack
from typing import Any


class Bank:
    """A collection of integer-balance accounts with atomic transfers."""

    __slots__ = ("_index", "_balances", "_locks")

    def __init__(self, balances: dict[Any, int]) -> None:
        if not isinstance(balances, dict):
            raise TypeError("balances must be a dictionary")

        snapshot = dict(balances)
        for balance in snapshot.values():
            if type(balance) is not int:
                raise TypeError("account balances must be integers")
            if balance < 0:
                raise ValueError("account balances cannot be negative")

        self._index = {
            account: position for position, account in enumerate(snapshot)
        }
        self._balances = list(snapshot.values())
        self._locks = [threading.Lock() for _ in snapshot]

    def _account_index(self, account: Any) -> int:
        try:
            return self._index[account]
        except (KeyError, TypeError):
            raise KeyError(account) from None

    def transfer(self, src: Any, dst: Any, amount: int) -> bool:
        """Atomically transfer an integer amount between two accounts."""
        src_index = self._account_index(src)
        dst_index = self._account_index(dst)

        if src_index == dst_index:
            raise ValueError("source and destination accounts must differ")
        if type(amount) is not int:
            raise TypeError("amount must be an integer")
        if amount < 0:
            raise ValueError("amount cannot be negative")

        first, second = sorted((src_index, dst_index))
        with self._locks[first]:
            with self._locks[second]:
                if self._balances[src_index] < amount:
                    return False
                self._balances[src_index] -= amount
                self._balances[dst_index] += amount
                return True

    def balance(self, account: Any) -> int:
        """Return the current balance of one account."""
        index = self._account_index(account)
        with self._locks[index]:
            return self._balances[index]

    def total(self) -> int:
        """Return an atomic snapshot of the sum of all balances."""
        with ExitStack() as stack:
            for lock in self._locks:
                stack.enter_context(lock)
            return sum(self._balances)
