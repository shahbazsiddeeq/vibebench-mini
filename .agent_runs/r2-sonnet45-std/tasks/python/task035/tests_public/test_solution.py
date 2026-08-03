import pytest
from src.solution import has_cycle


def test_self_loop():
    assert has_cycle([0]) is True


def test_single_terminal_node():
    assert has_cycle([-1]) is False


def test_two_nodes_no_cycle():
    # 0 -> 1 -> end
    assert has_cycle([1, -1]) is False


def test_chain_reaches_end_via_other_nodes():
    # 0 -> 2 -> 1 -> end
    assert has_cycle([2, -1, 1]) is False


def test_out_of_bounds_raises():
    with pytest.raises(ValueError):
        has_cycle([1, 5])
