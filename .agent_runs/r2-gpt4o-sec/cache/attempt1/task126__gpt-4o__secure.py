# src/solution.py

from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, nxt: 'Handler') -> 'Handler':
        self._next_handler = nxt
        return nxt

    @abstractmethod
    def handle(self, amount: int) -> str | None:
        pass

    def _validate_amount(self, amount):
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Amount must be an integer.")

class LowHandler(Handler):
    def handle(self, amount: int) -> str | None:
        self._validate_amount(amount)
        if amount < 100:
            return 'low'
        elif self._next_handler:
            return self._next_handler.handle(amount)
        return None

class MidHandler(Handler):
    def handle(self, amount: int) -> str | None:
        self._validate_amount(amount)
        if 100 <= amount < 1000:
            return 'mid'
        elif self._next_handler:
            return self._next_handler.handle(amount)
        return None

class HighHandler(Handler):
    def handle(self, amount: int) -> str | None:
        self._validate_amount(amount)
        if amount >= 1000:
            return 'high'
        elif self._next_handler:
            return self._next_handler.handle(amount)
        return None
