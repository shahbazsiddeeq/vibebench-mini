import math

class Shape:
    def _validate_dimension(self, dimension):
        if not isinstance(dimension, (int, float)) or isinstance(dimension, bool):
            raise ValueError("Dimension must be an int or float.")
        if dimension <= 0:
            raise ValueError("Dimension must be greater than 0.")
        return dimension

    def accept(self, visitor):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = self._validate_dimension(radius)

    def accept(self, visitor):
        return visitor.visit_circle(self)

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = self._validate_dimension(width)
        self.height = self._validate_dimension(height)

    def accept(self, visitor):
        return visitor.visit_rectangle(self)

class Square(Shape):
    def __init__(self, side):
        self.side = self._validate_dimension(side)

    def accept(self, visitor):
        return visitor.visit_square(self)

class AreaVisitor:
    def visit_circle(self, circle: Circle) -> float:
        return math.pi * circle.radius * circle.radius

    def visit_rectangle(self, rectangle: Rectangle) -> float:
        return float(rectangle.width * rectangle.height)

    def visit_square(self, square: Square) -> float:
        return float(square.side * square.side)

class PerimeterVisitor:
    def visit_circle(self, circle: Circle) -> float:
        return 2 * math.pi * circle.radius

    def visit_rectangle(self, rectangle: Rectangle) -> float:
        return 2 * float(rectangle.width + rectangle.height)

    def visit_square(self, square: Square) -> float:
        return 4 * float(square.side)

def total_area(shapes: list, visitor) -> float:
    required_methods = ['visit_circle', 'visit_rectangle', 'visit_square']
    for method_name in required_methods:
        if not hasattr(visitor, method_name) or not callable(getattr(visitor, method_name)):
            raise TypeError(f"Visitor must implement a callable '{method_name}' method.")

    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    return total
