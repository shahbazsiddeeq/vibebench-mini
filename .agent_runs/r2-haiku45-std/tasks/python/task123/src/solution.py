import math


class Circle:
    def __init__(self, radius):
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2


class Rectangle:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
        self.width = width
        self.height = height
    
    def area(self):
        return float(self.width * self.height)


class Square:
    def __init__(self, side):
        if side <= 0:
            raise ValueError("Side must be positive")
        self.side = side
    
    def area(self):
        return float(self.side ** 2)


def make_shape(kind: str, **kwargs) -> object:
    """
    Factory function to create shape objects.
    
    Args:
        kind: Type of shape ('circle', 'rectangle', 'square')
        **kwargs: Dimension parameters (radius, width/height, side)
    
    Returns:
        Shape object with .area() method
    
    Raises:
        ValueError: If kind is unknown or dimensions are non-positive
    """
    if kind == "circle":
        if "radius" not in kwargs:
            raise ValueError("Circle requires 'radius' parameter")
        return Circle(kwargs["radius"])
    elif kind == "rectangle":
        if "width" not in kwargs or "height" not in kwargs:
            raise ValueError("Rectangle requires 'width' and 'height' parameters")
        return Rectangle(kwargs["width"], kwargs["height"])
    elif kind == "square":
        if "side" not in kwargs:
            raise ValueError("Square requires 'side' parameter")
        return Square(kwargs["side"])
    else:
        raise ValueError(f"Unknown shape kind: {kind}")
