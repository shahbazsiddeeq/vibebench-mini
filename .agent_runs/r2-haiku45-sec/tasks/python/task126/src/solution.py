from typing import Optional


class Handler:
    """Base class for the Chain of Responsibility pattern."""
    
    def __init__(self) -> None:
        self._next: Optional[Handler] = None
    
    def set_next(self, nxt: "Handler") -> "Handler":
        """Set the next handler in the chain and return it for chaining."""
        self._next = nxt
        return nxt
    
    def handle(self, amount: int) -> Optional[str]:
        """Handle the amount or delegate to the next handler."""
        # Validate that amount is an integer (bool is a subclass of int, so exclude it)
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise ValueError("amount must be an integer")
        
        # Try to handle it
        result = self._handle_amount(amount)
        if result is not None:
            return result
        
        # Delegate to next handler if available
        if self._next is not None:
            return self._next.handle(amount)
        
        return None
    
    def _handle_amount(self, amount: int) -> Optional[str]:
        """Override in subclasses to define handling logic."""
        return None


class LowHandler(Handler):
    """Handles amounts less than 100."""
    
    def _handle_amount(self, amount: int) -> Optional[str]:
        if amount < 100:
            return "low"
        return None


class MidHandler(Handler):
    """Handles amounts from 100 to 999."""
    
    def _handle_amount(self, amount: int) -> Optional[str]:
        if 100 <= amount < 1000:
            return "mid"
        return None


class HighHandler(Handler):
    """Handles amounts 1000 and above."""
    
    def _handle_amount(self, amount: int) -> Optional[str]:
        if amount >= 1000:
            return "high"
        return None
