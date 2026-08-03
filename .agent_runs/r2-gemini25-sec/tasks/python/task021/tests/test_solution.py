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


def test_multi_hop():
    path = bfs_shortest_path(G, "A", "E")
    assert path[0] == "A" and path[-1] == "E"
    assert len(path) == 4


def test_same_node():
    assert bfs_shortest_path(G, "A", "A") == ["A"]


def test_no_path():
    disconnected = {"X": [], "Y": []}
    assert bfs_shortest_path(disconnected, "X", "Y") == []


def test_unknown_start():
    assert bfs_shortest_path(G, "Z", "A") == []


def test_two_node_graph():
    g = {"a": ["b"], "b": ["a"]}
    assert bfs_shortest_path(g, "a", "b") == ["a", "b"]


def test_linear_chain():
    g = {"1": ["2"], "2": ["1", "3"], "3": ["2", "4"], "4": ["3"]}
    assert bfs_shortest_path(g, "1", "4") == ["1", "2", "3", "4"]
