"""
Chain of Responsibility pattern implementation.

Provides a base Handler class and concrete handlers (LowHandler, MidHandler,
HighHandler) that classify an integer amount into a category by delegating
along a chain of responsibility.
"""

from __future__ import annotations

from typing import Optional


class Handler:
    """Base handler for the chain of responsibility pattern."""

    def __init__(self) -> None:
        self._next: Optional["Handler"] = None

    def set_next(self, nxt: "Handler") -> "Handler":
        """Set the next handler in the chain and return it for chaining."""
        if not isinstance(nxt, Handler):
            raise TypeError("nxt must be a Handler instance")
        self._next = nxt
        return nxt

    def handle(self, amount: int) -> Optional[str]:
        """
        Handle the amount or delegate to the next handler.

        Raises:
            ValueError: if amount is not an integer (bool excluded).
        """
        self._validate_amount(amount)
        return self._handle_validated(amount)

    @staticmethod
    def _validate_amount(amount: int) -> None:
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise ValueError("amount must be an integer (bool not allowed)")

    def _handle_validated(self, amount: int) -> Optional[str]:
        """
        Subclasses override this to attempt handling, delegating via
        self._delegate(amount) if they cannot handle it.
        """
        return self._delegate(amount)

    def _delegate(self, amount: int) -> Optional[str]:
        if self._next is not None:
            return self._next._handle_validated(amount)
        return None


class LowHandler(Handler):
    """Handles amounts less than 100."""

    def _handle_validated(self, amount: int) -> Optional[str]:
        if amount < 100:
            return "low"
        return self._delegate(amount)


class MidHandler(Handler):
    """Handles amounts in [100, 1000)."""

    def _handle_validated(self, amount: int) -> Optional[str]:
        if 100 <= amount < 1000:
            return "mid"
        return self._delegate(amount)


class HighHandler(Handler):
    """Handles amounts >= 1000."""

    def _handle_validated(self, amount: int) -> Optional[str]:
        if amount >= 1000:
            return "high"
        return self._delegate(amount)
