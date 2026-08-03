import math

class Circle:
    def __init__(self, radius):
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("Radius must be a positive number.")
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

class Rectangle:
    def __init__(self, width, height):
        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError("Width must be a positive number.")
        if not isinstance(height, (int, float)) or height <= 0:
            raise ValueError("Height must be a positive number.")
        self.width = width
        self.height = height

    def area(self):
        return float(self.width * self.height)

class Square:
    def __init__(self, side):
        if not isinstance(side, (int, float)) or side <= 0:
            raise ValueError("Side must be a positive number.")
        self.side = side

    def area(self):
        return float(self.side ** 2)

def make_shape(kind: str, **kwargs) -> object:
    if kind == 'circle':
        if 'radius' not in kwargs:
            raise ValueError("Missing 'radius' for circle.")
        return Circle(kwargs['radius'])
    elif kind == 'rectangle':
        if 'width' not in kwargs or 'height' not in kwargs:
            raise ValueError("Missing 'width' or 'height' for rectangle.")
        return Rectangle(kwargs['width'], kwargs['height'])
    elif kind == 'square':
        if 'side' not in kwargs:
            raise ValueError("Missing 'side' for square.")
        return Square(kwargs['side'])
    else:
        raise ValueError(f"Unknown shape kind: {kind}")
