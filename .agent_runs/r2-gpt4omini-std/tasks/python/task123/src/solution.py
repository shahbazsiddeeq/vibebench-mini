# src/solution.py

class Shape:
    def area(self) -> float:
        raise NotImplementedError("This method should be overridden by subclasses.")

class Circle(Shape):
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Radius must be positive.")
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * (self.radius ** 2)

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

class Square(Shape):
    def __init__(self, side: float):
        if side <= 0:
            raise ValueError("Side must be positive.")
        self.side = side

    def area(self) -> float:
        return self.side ** 2

def make_shape(kind: str, **kwargs) -> Shape:
    if kind == "circle":
        return Circle(kwargs.get("radius"))
    elif kind == "rectangle":
        return Rectangle(kwargs.get("width"), kwargs.get("height"))
    elif kind == "square":
        return Square(kwargs.get("side"))
    else:
        raise ValueError("Unknown shape kind.")
