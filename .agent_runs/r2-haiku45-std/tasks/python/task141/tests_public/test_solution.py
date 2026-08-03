import pytest

from src.solution import connected_components


def test_no_edges_all_singletons():
    assert connected_components(3, []) == [[0], [1], [2]]


def test_all_connected():
    assert connected_components(4, [(0, 1), (1, 2), (2, 3)]) == [[0, 1, 2, 3]]


def test_self_loops_and_duplicates_harmless():
    assert connected_components(3, [(0, 0), (1, 2), (1, 2), (2, 1)]) == [[0], [1, 2]]


def test_transitive_union_mutation_killer():
    # 0-1, 2-3, then 1-2 must merge into one component of all four.
    assert connected_components(4, [(0, 1), (2, 3), (1, 2)]) == [[0, 1, 2, 3]]


def test_out_of_range_endpoint_raises():
    with pytest.raises(ValueError):
        connected_components(3, [(0, 3)])
