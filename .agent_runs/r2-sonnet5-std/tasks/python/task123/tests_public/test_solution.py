from src.solution import make_shape
import math

import pytest


def test_rectangle_area():
    assert make_shape("rectangle", width=4, height=5).area() == 20.0


def test_returned_object_has_area_method():
    shape = make_shape("circle", radius=1)
    assert callable(shape.area)


def test_zero_dimension_raises():
    with pytest.raises(ValueError):
        make_shape("square", side=0)
