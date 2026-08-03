# src/solution.py

import math

class Shape:
    def accept(self, visitor):
        raise NotImplementedError("You should implement this method.")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = self._validate_dimension(radius)

    def _validate_dimension(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Dimension must be a positive int or float.")
        return value

    def accept(self, visitor):
        return visitor.visit_circle(self)

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = self._validate_dimension(width)
        self.height = self._validate_dimension(height)

    def _validate_dimension(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Dimension must be a positive int or float.")
        return value

    def accept(self, visitor):
        return visitor.visit_rectangle(self)

class Square(Shape):
    def __init__(self, side):
        self.side = self._validate_dimension(side)

    def _validate_dimension(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Dimension must be a positive int or float.")
        return value

    def accept(self, visitor):
        return visitor.visit_square(self)

class AreaVisitor:
    def visit_circle(self, circle):
        return math.pi * (circle.radius ** 2)

    def visit_rectangle(self, rectangle):
        return rectangle.width * rectangle.height

    def visit_square(self, square):
        return square.side ** 2

class PerimeterVisitor:
    def visit_circle(self, circle):
        return 2 * math.pi * circle.radius

    def visit_rectangle(self, rectangle):
        return 2 * (rectangle.width + rectangle.height)

    def visit_square(self, square):
        return 4 * square.side

def total_area(shapes, visitor):
    if not all(hasattr(visitor, method) for method in ['visit_circle', 'visit_rectangle', 'visit_square']):
        raise TypeError("Visitor must implement visit_circle, visit_rectangle, and visit_square methods.")
    
    return sum(shape.accept(visitor) for shape in shapes)
