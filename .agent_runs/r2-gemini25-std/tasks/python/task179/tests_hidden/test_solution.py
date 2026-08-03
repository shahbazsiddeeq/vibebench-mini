import sys
import threading
import time

import pytest

from src.solution import Bank


def test_negative_starting_balance_raises():
    with pytest.raises(ValueError):
        Bank({"a": 10, "b": -1})


def test_insufficient_funds_returns_false_no_change():
    bank = Bank({"a": 50, "b": 5})
    assert bank.transfer("a", "b", 1000) is False
    assert bank.balance("a") == 50
    assert bank.balance("b") == 5


def test_bad_amount_and_self_transfer_raise():
    bank = Bank({"a": 10, "b": 10})
    with pytest.raises(ValueError):
        bank.transfer("a", "b", -5)
    with pytest.raises(ValueError):
        bank.transfer("a", "a", 5)


def test_money_conserved_under_many_concurrent_transfers():
    # Missing/incorrect locking causes lost updates; total() would drift.
    accounts = {name: 1000 for name in "abcdef"}
    bank = Bank(accounts)
    start_total = bank.total()
    n_threads = 12
    per = 3000
    names = list(accounts)
    start = threading.Barrier(n_threads)

    def worker(seed):
        start.wait()
        x = seed
        for _ in range(per):
            x = (x * 1103515245 + 12345) & 0x7FFFFFFF
            i = x % len(names)
            j = (x >> 8) % len(names)
            if i == j:
                continue
            bank.transfer(names[i], names[j], 1)

    threads = [threading.Thread(target=worker, args=(s,)) for s in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
    assert all(not t.is_alive() for t in threads)
    assert bank.total() == start_total
    assert all(bank.balance(n) >= 0 for n in names)
