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


def test_perimeter_visitor_all_shapes():
    pv = PerimeterVisitor()
    assert Circle(2).accept(pv) == pytest.approx(4 * math.pi)
    assert Rectangle(3, 4).accept(pv) == pytest.approx(14.0)
    assert Square(5).accept(pv) == pytest.approx(20.0)


def test_total_area_sums():
    shapes = [Square(2), Rectangle(2, 3), Circle(1)]
    expected = 4.0 + 6.0 + math.pi
    assert total_area(shapes, AreaVisitor()) == pytest.approx(expected)


def test_total_area_rejects_incomplete_visitor():
    class Partial:
        def visit_circle(self, s):
            return 0.0

        def visit_rectangle(self, s):
            return 0.0

    with pytest.raises(TypeError):
        total_area([Square(1)], Partial())
