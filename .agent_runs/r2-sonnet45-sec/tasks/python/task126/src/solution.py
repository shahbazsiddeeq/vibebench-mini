class Handler:
    """Base handler class for the Chain of Responsibility pattern."""
    
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, nxt: 'Handler') -> 'Handler':
        """Set the next handler in the chain and return it for chaining."""
        self._next_handler = nxt
        return nxt
    
    def handle(self, amount: int) -> str | None:
        """
        Handle the request or delegate to the next handler.
        
        Args:
            amount: An integer amount to handle
            
        Returns:
            A string result if handled, None otherwise
            
        Raises:
            ValueError: If amount is not an integer (bool doesn't count)
        """
        # Validate input - must be int but not bool
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise ValueError("amount must be an integer")
        
        # Try to handle in subclass
        result = self._handle_request(amount)
        if result is not None:
            return result
        
        # Delegate to next handler if exists
        if self._next_handler is not None:
            return self._next_handler.handle(amount)
        
        return None
    
    def _handle_request(self, amount: int) -> str | None:
        """
        Subclasses override this to implement their handling logic.
        
        Args:
            amount: An integer amount to handle
            
        Returns:
            A string result if this handler can handle it, None otherwise
        """
        return None


class LowHandler(Handler):
    """Handler for amounts less than 100."""
    
    def _handle_request(self, amount: int) -> str | None:
        if amount < 100:
            return "low"
        return None


class MidHandler(Handler):
    """Handler for amounts between 100 (inclusive) and 1000 (exclusive)."""
    
    def _handle_request(self, amount: int) -> str | None:
        if 100 <= amount < 1000:
            return "mid"
        return None


class HighHandler(Handler):
    """Handler for amounts 1000 and above."""
    
    def _handle_request(self, amount: int) -> str | None:
        if amount >= 1000:
            return "high"
        return None
