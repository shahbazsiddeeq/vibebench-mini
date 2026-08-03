from __future__ import annotations

from typing import Optional


class Handler:
    def __init__(self) -> None:
        self._next: Optional[Handler] = None

    def set_next(self, nxt: Handler) -> Handler:
        self._next = nxt
        return nxt

    def handle(self, amount: int) -> Optional[str]:
        self._validate_amount(amount)
        return self._delegate(amount)

    @staticmethod
    def _validate_amount(amount: int) -> None:
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise ValueError("amount must be an integer")

    def _delegate(self, amount: int) -> Optional[str]:
        if self._next is None:
            return None
        return self._next.handle(amount)


class LowHandler(Handler):
    def handle(self, amount: int) -> Optional[str]:
        self._validate_amount(amount)
        if amount < 100:
            return "low"
        return self._delegate(amount)


class MidHandler(Handler):
    def handle(self, amount: int) -> Optional[str]:
        self._validate_amount(amount)
        if 100 <= amount < 1000:
            return "mid"
        return self._delegate(amount)


class HighHandler(Handler):
    def handle(self, amount: int) -> Optional[str]:
        self._validate_amount(amount)
        if amount >= 1000:
            return "high"
        return self._delegate(amount)
