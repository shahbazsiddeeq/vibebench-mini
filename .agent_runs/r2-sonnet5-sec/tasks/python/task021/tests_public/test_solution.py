from src.solution import bfs_shortest_path

G = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C", "E"],
    "E": ["D"],
}


def test_multi_hop():
    path = bfs_shortest_path(G, "A", "E")
    assert path[0] == "A" and path[-1] == "E"
    assert len(path) == 4


def test_no_path():
    disconnected = {"X": [], "Y": []}
    assert bfs_shortest_path(disconnected, "X", "Y") == []


def test_two_node_graph():
    g = {"a": ["b"], "b": ["a"]}
    assert bfs_shortest_path(g, "a", "b") == ["a", "b"]
