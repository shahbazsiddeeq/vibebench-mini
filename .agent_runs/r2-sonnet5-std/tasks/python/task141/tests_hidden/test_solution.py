import pytest

from src.solution import connected_components


def test_basic_two_components():
    assert connected_components(5, [(0, 1), (1, 2), (3, 4)]) == [[0, 1, 2], [3, 4]]


def test_zero_nodes():
    assert connected_components(0, []) == []


def test_isolated_node_with_edges():
    # Node 3 is isolated even though other nodes are joined.
    assert connected_components(4, [(0, 2)]) == [[0, 2], [1], [3]]


def test_outer_sorted_by_smallest_label():
    # Edges given out of order; output must still sort by smallest member.
    assert connected_components(6, [(4, 5), (0, 1), (2, 3)]) == [
        [0, 1],
        [2, 3],
        [4, 5],
    ]


def test_negative_n_raises():
    with pytest.raises(ValueError):
        connected_components(-1, [])


def test_negative_endpoint_raises():
    with pytest.raises(ValueError):
        connected_components(3, [(-1, 0)])
