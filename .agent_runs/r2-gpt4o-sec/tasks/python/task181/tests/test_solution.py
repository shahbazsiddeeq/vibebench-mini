import math

import pytest

from src.solution import (
    Circle,
    Rectangle,
    Square,
    AreaVisitor,
    PerimeterVisitor,
    total_area,
)


def test_worked_example():
    assert Square(3).accept(AreaVisitor()) == 9.0
    assert Rectangle(2, 5).accept(PerimeterVisitor()) == 14.0


def test_area_visitor_all_shapes():
    av = AreaVisitor()
    assert Circle(2).accept(av) == pytest.approx(math.pi * 4)
    assert Rectangle(3, 4).accept(av) == pytest.approx(12.0)
    assert Square(5).accept(av) == pytest.approx(25.0)


def test_perimeter_visitor_all_shapes():
    pv = PerimeterVisitor()
    assert Circle(2).accept(pv) == pytest.approx(4 * math.pi)
    assert Rectangle(3, 4).accept(pv) == pytest.approx(14.0)
    assert Square(5).accept(pv) == pytest.approx(20.0)


def test_dispatch_uses_correct_method():
    # A spy visitor proves accept dispatches to the right method (double dispatch).
    calls = []

    class Spy:
        def visit_circle(self, s):
            calls.append("circle")
            return 1.0

        def visit_rectangle(self, s):
            calls.append("rectangle")
            return 2.0

        def visit_square(self, s):
            calls.append("square")
            return 3.0

    Circle(1).accept(Spy())
    Square(1).accept(Spy())
    Rectangle(1, 1).accept(Spy())
    assert calls == ["circle", "square", "rectangle"]


def test_total_area_sums():
    shapes = [Square(2), Rectangle(2, 3), Circle(1)]
    expected = 4.0 + 6.0 + math.pi
    assert total_area(shapes, AreaVisitor()) == pytest.approx(expected)


def test_total_area_returns_float():
    assert isinstance(total_area([Square(1)], AreaVisitor()), float)


def test_total_area_rejects_incomplete_visitor():
    class Partial:
        def visit_circle(self, s):
            return 0.0

        def visit_rectangle(self, s):
            return 0.0

    with pytest.raises(TypeError):
        total_area([Square(1)], Partial())


def test_invalid_dimensions():
    with pytest.raises(ValueError):
        Circle(0)
    with pytest.raises(ValueError):
        Rectangle(-1, 2)
    with pytest.raises(ValueError):
        Square(True)
    with pytest.raises(ValueError):
        Rectangle("3", 4)
