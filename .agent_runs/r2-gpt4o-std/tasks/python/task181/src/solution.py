import math

class Shape:
    def accept(self, visitor):
        raise NotImplementedError("Must implement accept method")

class Circle(Shape):
    def __init__(self, radius):
        if not isinstance(radius, (int, float)) or isinstance(radius, bool) or radius <= 0:
            raise ValueError("Radius must be a positive number")
        self.radius = radius

    def accept(self, visitor):
        return visitor.visit_circle(self)

class Rectangle(Shape):
    def __init__(self, width, height):
        if not all(isinstance(dim, (int, float)) and not isinstance(dim, bool) and dim > 0 for dim in (width, height)):
            raise ValueError("Width and height must be positive numbers")
        self.width = width
        self.height = height

    def accept(self, visitor):
        return visitor.visit_rectangle(self)

class Square(Shape):
    def __init__(self, side):
        if not isinstance(side, (int, float)) or isinstance(side, bool) or side <= 0:
            raise ValueError("Side must be a positive number")
        self.side = side

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

def total_area(shapes, visitor):
    if not all(callable(getattr(visitor, method, None)) for method in ['visit_circle', 'visit_rectangle', 'visit_square']):
        raise TypeError("Visitor must implement visit_circle, visit_rectangle, and visit_square methods")
    
    return sum(shape.accept(visitor) for shape in shapes)
