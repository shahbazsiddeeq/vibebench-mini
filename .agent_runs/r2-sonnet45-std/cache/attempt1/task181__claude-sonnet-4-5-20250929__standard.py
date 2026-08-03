import math


def _validate_dimension(value, name="dimension"):
    """Validate that a dimension is a positive int or float (not bool)."""
    if isinstance(value, bool):
        raise ValueError(f"{name} cannot be a boolean")
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be an int or float")
    if value <= 0:
        raise ValueError(f"{name} must be > 0")


class Circle:
    def __init__(self, radius):
        _validate_dimension(radius, "radius")
        self.radius = radius
    
    def accept(self, visitor):
        return visitor.visit_circle(self)


class Rectangle:
    def __init__(self, width, height):
        _validate_dimension(width, "width")
        _validate_dimension(height, "height")
        self.width = width
        self.height = height
    
    def accept(self, visitor):
        return visitor.visit_rectangle(self)


class Square:
    def __init__(self, side):
        _validate_dimension(side, "side")
        self.side = side
    
    def accept(self, visitor):
        return visitor.visit_square(self)


class AreaVisitor:
    def visit_circle(self, circle):
        return float(math.pi * circle.radius * circle.radius)
    
    def visit_rectangle(self, rectangle):
        return float(rectangle.width * rectangle.height)
    
    def visit_square(self, square):
        return float(square.side * square.side)


class PerimeterVisitor:
    def visit_circle(self, circle):
        return float(2 * math.pi * circle.radius)
    
    def visit_rectangle(self, rectangle):
        return float(2 * (rectangle.width + rectangle.height))
    
    def visit_square(self, square):
        return float(4 * square.side)


def total_area(shapes: list, visitor) -> float:
    """
    Return the sum of shape.accept(visitor) over all shapes.
    Raises TypeError if visitor lacks any of the three visit_ methods.
    """
    # Check that visitor has all required methods before iterating
    required_methods = ['visit_circle', 'visit_rectangle', 'visit_square']
    for method_name in required_methods:
        if not hasattr(visitor, method_name):
            raise TypeError(f"visitor missing method: {method_name}")
        method = getattr(visitor, method_name)
        if not callable(method):
            raise TypeError(f"visitor.{method_name} is not callable")
    
    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    
    return float(total)
