from src.solution import bfs_shortest_path

G = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C", "E"],
    "E": ["D"],
}


def test_direct_neighbour():
    assert bfs_shortest_path(G, "A", "B") == ["A", "B"]


def test_same_node():
    assert bfs_shortest_path(G, "A", "A") == ["A"]


def test_unknown_start():
    assert bfs_shortest_path(G, "Z", "A") == []


def test_linear_chain():
    g = {"1": ["2"], "2": ["1", "3"], "3": ["2", "4"], "4": ["3"]}
    assert bfs_shortest_path(g, "1", "4") == ["1", "2", "3", "4"]
