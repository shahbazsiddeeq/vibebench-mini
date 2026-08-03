import contextlib
import threading


class Bank:
    """Accounts with per-account locks and deadlock-free atomic transfers."""

    def __init__(self, balances):
        for acct, bal in balances.items():
            if bal < 0:
                raise ValueError("starting balances must be non-negative")
        self._balances = dict(balances)
        # A stable global lock order (sorted account key) prevents deadlock:
        # every operation acquires the locks it needs in this same order.
        self._order = sorted(balances)
        self._locks = {acct: threading.Lock() for acct in balances}

    def transfer(self, src, dst, amount):
        if src not in self._balances:
            raise KeyError(src)
        if dst not in self._balances:
            raise KeyError(dst)
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if src == dst:
            raise ValueError("src and dst must differ")

        first, second = sorted((src, dst))
        with self._locks[first], self._locks[second]:
            if self._balances[src] < amount:
                return False
            self._balances[src] -= amount
            self._balances[dst] += amount
            return True

    def balance(self, account):
        if account not in self._balances:
            raise KeyError(account)
        with self._locks[account]:
            return self._balances[account]

    def total(self):
        # Acquire every account lock in the same global order used by transfer,
        # yielding a deadlock-free consistent snapshot of all balances.
        with contextlib.ExitStack() as stack:
            for acct in self._order:
                stack.enter_context(self._locks[acct])
            return sum(self._balances.values())
