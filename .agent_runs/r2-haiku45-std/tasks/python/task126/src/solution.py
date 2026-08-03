class Handler:
    def __init__(self):
        self._next = None
    
    def set_next(self, nxt: 'Handler') -> 'Handler':
        self._next = nxt
        return nxt
    
    def handle(self, amount: int) -> str | None:
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise ValueError("amount must be an integer")
        
        if self._can_handle(amount):
            return self._handle_amount(amount)
        elif self._next is not None:
            return self._next.handle(amount)
        else:
            return None
    
    def _can_handle(self, amount: int) -> bool:
        raise NotImplementedError
    
    def _handle_amount(self, amount: int) -> str:
        raise NotImplementedError


class LowHandler(Handler):
    def _can_handle(self, amount: int) -> bool:
        return amount < 100
    
    def _handle_amount(self, amount: int) -> str:
        return "low"


class MidHandler(Handler):
    def _can_handle(self, amount: int) -> bool:
        return 100 <= amount < 1000
    
    def _handle_amount(self, amount: int) -> str:
        return "mid"


class HighHandler(Handler):
    def _can_handle(self, amount: int) -> bool:
        return amount >= 1000
    
    def _handle_amount(self, amount: int) -> str:
        return "high"
