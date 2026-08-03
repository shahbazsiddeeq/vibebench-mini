import sys
import threading

import pytest

from src.solution import TokenBucket


def test_refill_capped_at_capacity():
    b = TokenBucket(2)
    b.allow(2)
    b.refill(5)
    assert b.tokens == 2
    assert b.allow(2) is True
    assert b.allow() is False


def test_allow_n_all_or_nothing():
    b = TokenBucket(3)
    assert b.allow(2) is True
    assert b.allow(2) is False  # only 1 left, consumes nothing
    assert b.allow(1) is True
