"""Chain of responsibility: classify an integer amount as low, mid or high."""
from __future__ import annotations

from typing import Optional


class Handler:
    """Base handler that validates input, then handles or delegates.

    Subclasses override ``_process`` with their handling rule; the shared input
    validation lives here in ``handle`` so it is not repeated per subclass.
    """

    def __init__(self) -> None:
        self._next: Optional["Handler"] = None

    def set_next(self, nxt: "Handler") -> "Handler":
        if not isinstance(nxt, Handler):
            raise ValueError("nxt must be a Handler")
        self._next = nxt
        return nxt

    def handle(self, amount: int) -> Optional[str]:
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("amount must be an integer")
        result = self._process(amount)
        if result is not None:
            return result
        if self._next is not None:
            return self._next.handle(amount)
        return None

    def _process(self, amount: int) -> Optional[str]:
        """Return a label if this handler handles the amount, else None."""
        return None


class LowHandler(Handler):
    def _process(self, amount: int) -> Optional[str]:
        return "low" if amount < 100 else None


class MidHandler(Handler):
    def _process(self, amount: int) -> Optional[str]:
        return "mid" if 100 <= amount < 1000 else None


class HighHandler(Handler):
    def _process(self, amount: int) -> Optional[str]:
        return "high" if amount >= 1000 else None
