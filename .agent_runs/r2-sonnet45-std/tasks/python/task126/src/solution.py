class Handler:
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, nxt: 'Handler') -> 'Handler':
        self._next_handler = nxt
        return nxt
    
    def handle(self, amount: int) -> str | None:
        # Validate that amount is an integer but not a bool
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise ValueError("Amount must be an integer")
        
        # Try to handle the request
        result = self._handle_request(amount)
        if result is not None:
            return result
        
        # Delegate to next handler if exists
        if self._next_handler is not None:
            return self._next_handler.handle(amount)
        
        return None
    
    def _handle_request(self, amount: int) -> str | None:
        # Base implementation - subclasses override this
        return None


class LowHandler(Handler):
    def _handle_request(self, amount: int) -> str | None:
        if amount < 100:
            return 'low'
        return None


class MidHandler(Handler):
    def _handle_request(self, amount: int) -> str | None:
        if 100 <= amount < 1000:
            return 'mid'
        return None


class HighHandler(Handler):
    def _handle_request(self, amount: int) -> str | None:
        if amount >= 1000:
            return 'high'
        return None
