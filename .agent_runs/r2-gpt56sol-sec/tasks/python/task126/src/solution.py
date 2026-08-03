from __future__ import annotations

from typing import Optional


class Handler:
    """Base handler for a chain of responsibility."""

    def __init__(self) -> None:
        self._next_handler: Optional[Handler] = None

    def set_next(self, nxt: Handler) -> Handler:
        """Set and return the next handler in the chain."""
        if not isinstance(nxt, Handler):
            raise TypeError("next handler must be a Handler")
        self._next_handler = nxt
        return nxt

    def handle(self, amount: int) -> Optional[str]:
        """Handle an integer amount or delegate to the next handler."""
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise ValueError("amount must be an integer")

        current: Optional[Handler] = self
        visited: set[int] = set()

        while current is not None:
            identity = id(current)
            if identity in visited:
                return None
            visited.add(identity)

            result = current._handle_amount(amount)
            if result is not None:
                return result
            current = current._next_handler

        return None

    def _handle_amount(self, amount: int) -> Optional[str]:
        return None


class LowHandler(Handler):
    """Handles amounts below 100."""

    def _handle_amount(self, amount: int) -> Optional[str]:
        return "low" if amount < 100 else None


class MidHandler(Handler):
    """Handles amounts from 100 through 999."""

    def _handle_amount(self, amount: int) -> Optional[str]:
        return "mid" if 100 <= amount < 1000 else None


class HighHandler(Handler):
    """Handles amounts of 1000 or greater."""

    def _handle_amount(self, amount: int) -> Optional[str]:
        return "high" if amount >= 1000 else None
