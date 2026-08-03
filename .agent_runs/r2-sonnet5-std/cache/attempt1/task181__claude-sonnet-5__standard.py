import math


def _validate_dimension(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Dimension must be an int or float (not bool)")
    if value <= 0:
        raise ValueError("Dimension must be > 0")


class Circle:
    def __init__(self, radius):
        _validate_dimension(radius)
        self.radius = radius

    def accept(self, visitor):
        return visitor.visit_circle(self)


class Rectangle:
    def __init__(self, width, height):
        _validate_dimension(width)
        _validate_dimension(height)
        self.width = width
        self.height = height

    def accept(self, visitor):
        return visitor.visit_rectangle(self)


class Square:
    def __init__(self, side):
        _validate_dimension(side)
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


def total_area(shapes, visitor):
    for method_name in ("visit_circle", "visit_rectangle", "visit_square"):
        if not callable(getattr(visitor, method_name, None)):
            raise TypeError(
                f"visitor is missing callable attribute '{method_name}'"
            )

    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    return float(total)
