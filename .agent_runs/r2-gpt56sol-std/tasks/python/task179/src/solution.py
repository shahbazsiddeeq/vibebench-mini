from __future__ import annotations

import threading
from typing import Hashable, Mapping


class Bank:
    """A thread-safe collection of accounts supporting atomic transfers."""

    def __init__(self, balances: Mapping[Hashable, int]):
        initial = dict(balances)
        if any(balance < 0 for balance in initial.values()):
            raise ValueError("starting balances cannot be negative")

        self._balances = initial
        self._order = {account: index for index, account in enumerate(initial)}
        self._locks = {account: threading.Lock() for account in initial}

    def transfer(
        self,
        src: Hashable,
        dst: Hashable,
        amount: int,
    ) -> bool:
        if src not in self._balances:
            raise KeyError(src)
        if dst not in self._balances:
            raise KeyError(dst)
        if amount < 0:
            raise ValueError("transfer amount cannot be negative")
        if src == dst:
            raise ValueError("source and destination must be different")

        if self._order[src] < self._order[dst]:
            first, second = src, dst
        else:
            first, second = dst, src

        first_lock = self._locks[first]
        second_lock = self._locks[second]

        with first_lock:
            with second_lock:
                if self._balances[src] < amount:
                    return False
                self._balances[src] -= amount
                self._balances[dst] += amount
                return True

    def balance(self, account: Hashable) -> int:
        if account not in self._balances:
            raise KeyError(account)

        with self._locks[account]:
            return self._balances[account]

    def total(self) -> int:
        acquired = []
        try:
            for account in self._balances:
                lock = self._locks[account]
                lock.acquire()
                acquired.append(lock)
            return sum(self._balances.values())
        finally:
            for lock in reversed(acquired):
                lock.release()
