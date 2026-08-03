import math


class _Shape:
    def area(self) -> float:
        raise NotImplementedError


class _Circle(_Shape):
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("radius must be positive")
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2


class _Rectangle(_Shape):
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        self.width = width
        self.height = height

    def area(self) -> float:
        return float(self.width * self.height)


class _Square(_Shape):
    def __init__(self, side: float):
        if side <= 0:
            raise ValueError("side must be positive")
        self.side = side

    def area(self) -> float:
        return float(self.side ** 2)


def make_shape(kind: str, **kwargs) -> object:
    kind = kind.lower()
    if kind == "circle":
        return _Circle(**kwargs)
    elif kind == "rectangle":
        return _Rectangle(**kwargs)
    elif kind == "square":
        return _Square(**kwargs)
    else:
        raise ValueError(f"Unknown shape kind: {kind}")
