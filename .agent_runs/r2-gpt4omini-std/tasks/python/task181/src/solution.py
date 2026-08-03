import math

class Shape:
    def accept(self, visitor):
        raise NotImplementedError("You should implement this method.")

class Circle(Shape):
    def __init__(self, radius):
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("Radius must be a positive number.")
        self.radius = radius

    def accept(self, visitor):
        return visitor.visit_circle(self)

class Rectangle(Shape):
    def __init__(self, width, height):
        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError("Width must be a positive number.")
        if not isinstance(height, (int, float)) or height <= 0:
            raise ValueError("Height must be a positive number.")
        self.width = width
        self.height = height

    def accept(self, visitor):
        return visitor.visit_rectangle(self)

class Square(Shape):
    def __init__(self, side):
        if not isinstance(side, (int, float)) or side <= 0:
            raise ValueError("Side must be a positive number.")
        self.side = side

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
