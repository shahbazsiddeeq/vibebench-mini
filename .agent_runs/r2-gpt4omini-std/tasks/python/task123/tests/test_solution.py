from src.solution import make_shape
import math

import pytest


def test_square_area():
    assert make_shape("square", side=3).area() == 9.0


def test_rectangle_area():
    assert make_shape("rectangle", width=4, height=5).area() == 20.0


def test_circle_area():
    shape = make_shape("circle", radius=2)
    assert math.isclose(shape.area(), math.pi * 4)


def test_returned_object_has_area_method():
    shape = make_shape("circle", radius=1)
    assert callable(shape.area)


def test_unknown_kind_raises():
    with pytest.raises(ValueError):
        make_shape("triangle", base=3, height=4)


def test_zero_dimension_raises():
    with pytest.raises(ValueError):
        make_shape("square", side=0)


def test_negative_dimension_raises():
    with pytest.raises(ValueError):
        make_shape("rectangle", width=4, height=-1)
