import pytest

from src.solution import dijkstra


def test_shorter_indirect_route_mutation_killer():
    # Direct A->C is 4, but A->B->C is 3; must pick 3.
    graph = {"A": [("B", 1), ("C", 4)], "B": [("C", 2)], "C": []}
    assert dijkstra(graph, "A")["C"] == 3


def test_unreachable_nodes_omitted():
    graph = {"A": [("B", 2)], "B": [], "C": [("A", 1)]}
    # C is not reachable from A.
    assert dijkstra(graph, "A") == {"A": 0, "B": 2}


def test_chain():
    graph = {"A": [("B", 1)], "B": [("C", 1)], "C": [("D", 1)], "D": []}
    assert dijkstra(graph, "A") == {"A": 0, "B": 1, "C": 2, "D": 3}


def test_start_not_in_graph_raises():
    with pytest.raises(ValueError):
        dijkstra({"A": []}, "Z")


def test_large_line_graph_scales():
    n = 5000
    graph = {i: [(i + 1, 1)] for i in range(n)}
    graph[n] = []
    result = dijkstra(graph, 0)
    assert result[n] == n
    assert len(result) == n + 1
