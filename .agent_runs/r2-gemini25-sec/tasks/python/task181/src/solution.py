import math

class Shape:
    def _validate_dimension(self, dimension, name):
        if not isinstance(dimension, (int, float)) or isinstance(dimension, bool):
            raise ValueError(f"{name} must be an int or float.")
        if dimension <= 0:
            raise ValueError(f"{name} must be greater than 0.")
        return float(dimension)

    def accept(self, visitor):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = self._validate_dimension(radius, "radius")

    def accept(self, visitor):
        return visitor.visit_circle(self)

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = self._validate_dimension(width, "width")
        self.height = self._validate_dimension(height, "height")

    def accept(self, visitor):
        return visitor.visit_rectangle(self)

class Square(Shape):
    def __init__(self, side):
        self.side = self._validate_dimension(side, "side")

    def accept(self, visitor):
        return visitor.visit_square(self)

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

def total_area(shapes: list, visitor) -> float:
    required_methods = ["visit_circle", "visit_rectangle", "visit_square"]
    for method_name in required_methods:
        if not hasattr(visitor, method_name) or not callable(getattr(visitor, method_name)):
            raise TypeError(f"Visitor must have a callable '{method_name}' method.")

    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    return total
