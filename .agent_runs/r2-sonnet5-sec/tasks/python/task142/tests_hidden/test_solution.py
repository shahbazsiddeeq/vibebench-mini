import pytest

from src.solution import dijkstra


def test_basic_example():
    graph = {"A": [("B", 1), ("C", 4)], "B": [("C", 2)], "C": []}
    assert dijkstra(graph, "A") == {"A": 0, "B": 1, "C": 3}


def test_start_only():
    assert dijkstra({"X": []}, "X") == {"X": 0}


def test_neighbor_only_node_is_reachable():
    # 'D' only appears as a neighbor; still gets a distance, no outgoing edges.
    graph = {"A": [("D", 5)]}
    assert dijkstra(graph, "A") == {"A": 0, "D": 5}


def test_integer_nodes_and_cycle():
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    assert dijkstra(graph, 0) == {0: 0, 1: 3, 2: 1, 3: 4}


def test_negative_weight_raises():
    with pytest.raises(ValueError):
        dijkstra({"A": [("B", -1)], "B": []}, "A")
