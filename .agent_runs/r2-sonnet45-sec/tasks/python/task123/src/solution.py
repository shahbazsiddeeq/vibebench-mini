import math


class Circle:
    """Circle shape with radius."""
    
    def __init__(self, radius):
        if not isinstance(radius, (int, float)):
            raise ValueError("radius must be a number")
        if radius <= 0:
            raise ValueError("radius must be positive")
        self._radius = float(radius)
    
    def area(self):
        """Calculate and return the area of the circle."""
        return math.pi * self._radius * self._radius


class Rectangle:
    """Rectangle shape with width and height."""
    
    def __init__(self, width, height):
        if not isinstance(width, (int, float)):
            raise ValueError("width must be a number")
        if not isinstance(height, (int, float)):
            raise ValueError("height must be a number")
        if width <= 0:
            raise ValueError("width must be positive")
        if height <= 0:
            raise ValueError("height must be positive")
        self._width = float(width)
        self._height = float(height)
    
    def area(self):
        """Calculate and return the area of the rectangle."""
        return self._width * self._height


class Square:
    """Square shape with side length."""
    
    def __init__(self, side):
        if not isinstance(side, (int, float)):
            raise ValueError("side must be a number")
        if side <= 0:
            raise ValueError("side must be positive")
        self._side = float(side)
    
    def area(self):
        """Calculate and return the area of the square."""
        return self._side * self._side


def make_shape(kind, **kwargs):
    """
    Factory function to create shape objects.
    
    Args:
        kind: Type of shape ('circle', 'rectangle', 'square')
        **kwargs: Dimensions for the shape
            - circle: radius
            - rectangle: width, height
            - square: side
    
    Returns:
        A shape object with an area() method
    
    Raises:
        ValueError: If kind is unknown or dimensions are invalid
    """
    if not isinstance(kind, str):
        raise ValueError("kind must be a string")
    
    kind = kind.lower().strip()
    
    if kind == "circle":
        if "radius" not in kwargs:
            raise ValueError("circle requires 'radius' parameter")
        return Circle(kwargs["radius"])
    elif kind == "rectangle":
        if "width" not in kwargs:
            raise ValueError("rectangle requires 'width' parameter")
        if "height" not in kwargs:
            raise ValueError("rectangle requires 'height' parameter")
        return Rectangle(kwargs["width"], kwargs["height"])
    elif kind == "square":
        if "side" not in kwargs:
            raise ValueError("square requires 'side' parameter")
        return Square(kwargs["side"])
    else:
        raise ValueError(f"unknown shape kind: {kind}")
