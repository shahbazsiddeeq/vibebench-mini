import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate and return the area of the shape."""
        pass


class Circle(Shape):
    """Circle shape with radius."""
    
    def __init__(self, radius: float):
        if not isinstance(radius, (int, float)):
            raise ValueError("radius must be a number")
        if radius <= 0:
            raise ValueError("radius must be positive")
        self.radius = radius
    
    def area(self) -> float:
        """Calculate the area of the circle."""
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    """Rectangle shape with width and height."""
    
    def __init__(self, width: float, height: float):
        if not isinstance(width, (int, float)):
            raise ValueError("width must be a number")
        if not isinstance(height, (int, float)):
            raise ValueError("height must be a number")
        if width <= 0:
            raise ValueError("width must be positive")
        if height <= 0:
            raise ValueError("height must be positive")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        """Calculate the area of the rectangle."""
        return self.width * self.height


class Square(Shape):
    """Square shape with side length."""
    
    def __init__(self, side: float):
        if not isinstance(side, (int, float)):
            raise ValueError("side must be a number")
        if side <= 0:
            raise ValueError("side must be positive")
        self.side = side
    
    def area(self) -> float:
        """Calculate the area of the square."""
        return self.side ** 2


def make_shape(kind: str, **kwargs) -> Shape:
    """
    Factory function to create shape objects.
    
    Args:
        kind: The type of shape ('circle', 'rectangle', or 'square')
        **kwargs: Shape-specific parameters
            - circle: radius
            - rectangle: width, height
            - square: side
    
    Returns:
        A Shape object with an area() method
    
    Raises:
        ValueError: If kind is unknown or dimensions are non-positive
    """
    if not isinstance(kind, str):
        raise ValueError("kind must be a string")
    
    kind = kind.lower().strip()
    
    if kind == "circle":
        if "radius" not in kwargs:
            raise ValueError("circle requires 'radius' parameter")
        return Circle(kwargs["radius"])
    
    elif kind == "rectangle":
        if "width" not in kwargs or "height" not in kwargs:
            raise ValueError("rectangle requires 'width' and 'height' parameters")
        return Rectangle(kwargs["width"], kwargs["height"])
    
    elif kind == "square":
        if "side" not in kwargs:
            raise ValueError("square requires 'side' parameter")
        return Square(kwargs["side"])
    
    else:
        raise ValueError(f"unknown shape kind: {kind}")
