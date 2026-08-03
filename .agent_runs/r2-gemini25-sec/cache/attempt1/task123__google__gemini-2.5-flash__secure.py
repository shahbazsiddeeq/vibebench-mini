import math

class Shape:
    def area(self) -> float:
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius: float):
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("Radius must be a positive number.")
        self.radius = float(radius)

    def area(self) -> float:
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError("Width must be a positive number.")
        if not isinstance(height, (int, float)) or height <= 0:
            raise ValueError("Height must be a positive number.")
        self.width = float(width)
        self.height = float(height)

    def area(self) -> float:
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side: float):
        super().__init__(width=side, height=side)
        if not isinstance(side, (int, float)) or side <= 0:
            raise ValueError("Side must be a positive number.")
        self.side = float(side) # Store for consistency, though parent handles validation

def make_shape(kind: str, **kwargs) -> Shape:
    if not isinstance(kind, str):
        raise ValueError("Shape kind must be a string.")

    kind_lower = kind.lower()

    if kind_lower == 'circle':
        if 'radius' not in kwargs:
            raise ValueError("Circle requires 'radius' argument.")
        return Circle(kwargs['radius'])
    elif kind_lower == 'rectangle':
        if 'width' not in kwargs or 'height' not in kwargs:
            raise ValueError("Rectangle requires 'width' and 'height' arguments.")
        return Rectangle(kwargs['width'], kwargs['height'])
    elif kind_lower == 'square':
        if 'side' not in kwargs:
            raise ValueError("Square requires 'side' argument.")
        return Square(kwargs['side'])
    else:
        raise ValueError(f"Unknown shape kind: {kind}")
