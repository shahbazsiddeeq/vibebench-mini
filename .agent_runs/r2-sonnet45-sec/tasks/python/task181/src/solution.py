import math
from typing import Protocol, List


def _validate_dimension(value, name: str = "dimension"):
    """Validate that a dimension is a positive int or float (not bool)."""
    # Reject bool explicitly (bool is a subclass of int in Python)
    if isinstance(value, bool):
        raise ValueError(f"{name} cannot be a boolean")
    
    # Check if it's int or float
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be an int or float")
    
    # Check if positive
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0")
    
    return float(value)


class Circle:
    """Circle shape with radius."""
    
    def __init__(self, radius):
        self.radius = _validate_dimension(radius, "radius")
    
    def accept(self, visitor):
        """Accept a visitor and dispatch to visit_circle."""
        return visitor.visit_circle(self)


class Rectangle:
    """Rectangle shape with width and height."""
    
    def __init__(self, width, height):
        self.width = _validate_dimension(width, "width")
        self.height = _validate_dimension(height, "height")
    
    def accept(self, visitor):
        """Accept a visitor and dispatch to visit_rectangle."""
        return visitor.visit_rectangle(self)


class Square:
    """Square shape with side length."""
    
    def __init__(self, side):
        self.side = _validate_dimension(side, "side")
    
    def accept(self, visitor):
        """Accept a visitor and dispatch to visit_square."""
        return visitor.visit_square(self)


class AreaVisitor:
    """Visitor that calculates the area of shapes."""
    
    def visit_circle(self, circle: Circle) -> float:
        """Calculate area of a circle: pi * r^2."""
        return math.pi * circle.radius * circle.radius
    
    def visit_rectangle(self, rectangle: Rectangle) -> float:
        """Calculate area of a rectangle: width * height."""
        return rectangle.width * rectangle.height
    
    def visit_square(self, square: Square) -> float:
        """Calculate area of a square: side^2."""
        return square.side * square.side


class PerimeterVisitor:
    """Visitor that calculates the perimeter of shapes."""
    
    def visit_circle(self, circle: Circle) -> float:
        """Calculate perimeter (circumference) of a circle: 2 * pi * r."""
        return 2 * math.pi * circle.radius
    
    def visit_rectangle(self, rectangle: Rectangle) -> float:
        """Calculate perimeter of a rectangle: 2 * (width + height)."""
        return 2 * (rectangle.width + rectangle.height)
    
    def visit_square(self, square: Square) -> float:
        """Calculate perimeter of a square: 4 * side."""
        return 4 * square.side


def total_area(shapes: list, visitor) -> float:
    """
    Calculate the total area/perimeter of all shapes using the given visitor.
    
    Args:
        shapes: List of shape objects
        visitor: Visitor object with visit_circle, visit_rectangle, visit_square methods
    
    Returns:
        Sum of visitor results for all shapes as a float
    
    Raises:
        TypeError: If visitor lacks any required visit methods
    """
    # Validate that visitor has all required methods before processing
    required_methods = ['visit_circle', 'visit_rectangle', 'visit_square']
    
    for method_name in required_methods:
        if not hasattr(visitor, method_name):
            raise TypeError(f"Visitor missing required method: {method_name}")
        
        method = getattr(visitor, method_name)
        if not callable(method):
            raise TypeError(f"Visitor attribute {method_name} is not callable")
    
    # Calculate total by accepting visitor for each shape
    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    
    return float(total)
