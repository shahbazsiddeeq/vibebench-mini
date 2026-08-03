import math
from typing import List
import secrets

class Shape:
    def accept(self, visitor):
        raise NotImplementedError("Must implement accept method")

class Circle(Shape):
    def __init__(self, radius):
        self._validate_dimension(radius)
        self.radius = radius

    def accept(self, visitor):
        return visitor.visit_circle(self)

    @staticmethod
    def _validate_dimension(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            raise ValueError("Dimension must be a positive int or float")

class Rectangle(Shape):
    def __init__(self, width, height):
        self._validate_dimension(width)
        self._validate_dimension(height)
        self.width = width
        self.height = height

    def accept(self, visitor):
        return visitor.visit_rectangle(self)

    @staticmethod
    def _validate_dimension(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            raise ValueError("Dimension must be a positive int or float")

class Square(Shape):
    def __init__(self, side):
        self._validate_dimension(side)
        self.side = side

    def accept(self, visitor):
        return visitor.visit_square(self)

    @staticmethod
    def _validate_dimension(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            raise ValueError("Dimension must be a positive int or float")

class AreaVisitor:
    def visit_circle(self, circle):
        return math.pi * circle.radius * circle.radius

    def visit_rectangle(self, rectangle):
        return rectangle.width * rectangle.height

    def visit_square(self, square):
        return square.side * square.side

class PerimeterVisitor:
    def visit_circle(self, circle):
        return 2 * math.pi * circle.radius

    def visit_rectangle(self, rectangle):
        return 2 * (rectangle.width + rectangle.height)

    def visit_square(self, square):
        return 4 * square.side

def total_area(shapes: List[Shape], visitor) -> float:
    if not all(callable(getattr(visitor, method, None)) for method in ['visit_circle', 'visit_rectangle', 'visit_square']):
        raise TypeError("Visitor must implement visit_circle, visit_rectangle, and visit_square methods")
    
    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    return total
