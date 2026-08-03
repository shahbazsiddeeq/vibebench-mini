import math
from typing import List


class Circle:
    def __init__(self, radius):
        if isinstance(radius, bool) or not isinstance(radius, (int, float)):
            raise ValueError("Radius must be a number (not bool)")
        if radius <= 0:
            raise ValueError("Radius must be > 0")
        self.radius = radius
    
    def accept(self, visitor):
        return visitor.visit_circle(self)


class Rectangle:
    def __init__(self, width, height):
        if isinstance(width, bool) or not isinstance(width, (int, float)):
            raise ValueError("Width must be a number (not bool)")
        if isinstance(height, bool) or not isinstance(height, (int, float)):
            raise ValueError("Height must be a number (not bool)")
        if width <= 0:
            raise ValueError("Width must be > 0")
        if height <= 0:
            raise ValueError("Height must be > 0")
        self.width = width
        self.height = height
    
    def accept(self, visitor):
        return visitor.visit_rectangle(self)


class Square:
    def __init__(self, side):
        if isinstance(side, bool) or not isinstance(side, (int, float)):
            raise ValueError("Side must be a number (not bool)")
        if side <= 0:
            raise ValueError("Side must be > 0")
        self.side = side
    
    def accept(self, visitor):
        return visitor.visit_square(self)


class AreaVisitor:
    def visit_circle(self, shape):
        return math.pi * shape.radius * shape.radius
    
    def visit_rectangle(self, shape):
        return float(shape.width * shape.height)
    
    def visit_square(self, shape):
        return float(shape.side * shape.side)


class PerimeterVisitor:
    def visit_circle(self, shape):
        return 2 * math.pi * shape.radius
    
    def visit_rectangle(self, shape):
        return float(2 * (shape.width + shape.height))
    
    def visit_square(self, shape):
        return float(4 * shape.side)


def total_area(shapes: List, visitor) -> float:
    # Check that visitor has all required methods
    required_methods = ['visit_circle', 'visit_rectangle', 'visit_square']
    for method in required_methods:
        if not callable(getattr(visitor, method, None)):
            raise TypeError(f"Visitor must have callable {method} method")
    
    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    return total
