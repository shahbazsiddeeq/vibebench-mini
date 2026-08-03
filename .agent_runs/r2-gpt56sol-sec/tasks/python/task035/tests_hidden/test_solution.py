import pytest
from src.solution import has_cycle


def test_cycle_three_nodes():
    # 0 -> 1 -> 2 -> 0
    assert has_cycle([1, 2, 0]) is True


def test_no_cycle_linear():
    # 0 -> 1 -> 2 -> end
    assert has_cycle([1, 2, -1]) is False


def test_two_nodes_cycle():
    assert has_cycle([1, 0]) is True


def test_chain_into_cycle_not_containing_start():
    # 0 -> 1 -> 2 -> 3 -> 1 (cycle among 1,2,3)
    assert has_cycle([1, 2, 3, 1]) is True


def test_empty():
    assert has_cycle([]) is False


def test_index_below_negative_one_raises():
    with pytest.raises(ValueError):
        has_cycle([-2, 0])
