import math
from typing import List, Any


class Circle:
    def __init__(self, radius):
        self._validate_dimension(radius, "radius")
        self.radius = radius
    
    @staticmethod
    def _validate_dimension(value, name):
        # Reject bool explicitly (bool is a subclass of int in Python)
        if isinstance(value, bool):
            raise ValueError(f"{name} must be a number, not bool")
        # Accept int or float
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be int or float")
        # Must be positive
        if value <= 0:
            raise ValueError(f"{name} must be > 0")
    
    def accept(self, visitor):
        return visitor.visit_circle(self)


class Rectangle:
    def __init__(self, width, height):
        self._validate_dimension(width, "width")
        self._validate_dimension(height, "height")
        self.width = width
        self.height = height
    
    @staticmethod
    def _validate_dimension(value, name):
        # Reject bool explicitly (bool is a subclass of int in Python)
        if isinstance(value, bool):
            raise ValueError(f"{name} must be a number, not bool")
        # Accept int or float
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be int or float")
        # Must be positive
        if value <= 0:
            raise ValueError(f"{name} must be > 0")
    
    def accept(self, visitor):
        return visitor.visit_rectangle(self)


class Square:
    def __init__(self, side):
        self._validate_dimension(side, "side")
        self.side = side
    
    @staticmethod
    def _validate_dimension(value, name):
        # Reject bool explicitly (bool is a subclass of int in Python)
        if isinstance(value, bool):
            raise ValueError(f"{name} must be a number, not bool")
        # Accept int or float
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be int or float")
        # Must be positive
        if value <= 0:
            raise ValueError(f"{name} must be > 0")
    
    def accept(self, visitor):
        return visitor.visit_square(self)


class AreaVisitor:
    def visit_circle(self, shape: Circle) -> float:
        return math.pi * shape.radius * shape.radius
    
    def visit_rectangle(self, shape: Rectangle) -> float:
        return float(shape.width * shape.height)
    
    def visit_square(self, shape: Square) -> float:
        return float(shape.side * shape.side)


class PerimeterVisitor:
    def visit_circle(self, shape: Circle) -> float:
        return 2 * math.pi * shape.radius
    
    def visit_rectangle(self, shape: Rectangle) -> float:
        return 2 * (shape.width + shape.height)
    
    def visit_square(self, shape: Square) -> float:
        return 4 * shape.side


def total_area(shapes: List[Any], visitor: Any) -> float:
    # Validate that visitor has all required methods
    required_methods = ['visit_circle', 'visit_rectangle', 'visit_square']
    for method_name in required_methods:
        if not callable(getattr(visitor, method_name, None)):
            raise TypeError(f"visitor must have callable {method_name} method")
    
    # Sum up areas by accepting visitor on each shape
    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    
    return total
