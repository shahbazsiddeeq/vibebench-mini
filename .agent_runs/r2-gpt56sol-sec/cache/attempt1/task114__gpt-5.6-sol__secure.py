"""Topological sorting for directed graphs."""

from collections import deque
from collections.abc import Iterable, Mapping
from typing import Any


def topo_sort(graph: Mapping[Any, Iterable[Any]]) -> list[Any]:
    """Return a topological ordering of nodes in a directed graph.

    Nodes appearing only as neighbors are included in the result.

    Args:
        graph: A mapping from each node to an iterable of its outgoing
            neighbors.

    Raises:
        TypeError: If the graph or its adjacency lists are invalid, or if a
            node is not hashable.
        ValueError: If the graph contains a directed cycle.
    """
    if not isinstance(graph, Mapping):
        raise TypeError("graph must be a mapping")

    adjacency: dict[Any, list[Any]] = {}
    node_order: list[Any] = []
    known_nodes: set[Any] = set()

    def register_node(node: Any) -> None:
        try:
            if node not in known_nodes:
                known_nodes.add(node)
                node_order.append(node)
        except TypeError:
            raise TypeError("all graph nodes must be hashable") from None

    try:
        items = list(graph.items())
    except (TypeError, RuntimeError):
        raise TypeError("graph must be a valid mapping") from None

    for node, _ in items:
        register_node(node)

    for node, neighbors in items:
        if isinstance(neighbors, (str, bytes, bytearray)) or not isinstance(
            neighbors, Iterable
        ):
            raise TypeError("each adjacency list must be a non-string iterable")

        unique_neighbors: list[Any] = []
        seen: set[Any] = set()

        try:
            for neighbor in neighbors:
                register_node(neighbor)
                if neighbor not in seen:
                    seen.add(neighbor)
                    unique_neighbors.append(neighbor)
        except TypeError as exc:
            if str(exc) == "all graph nodes must be hashable":
                raise
            raise TypeError("all graph nodes must be hashable") from None
        except RuntimeError:
            raise TypeError("adjacency lists must remain stable during iteration") from None

        adjacency[node] = unique_neighbors

    for node in node_order:
        adjacency.setdefault(node, [])

    indegree = {node: 0 for node in node_order}
    for neighbors in adjacency.values():
        for neighbor in neighbors:
            indegree[neighbor] += 1

    ready = deque(node for node in node_order if indegree[node] == 0)
    result: list[Any] = []

    while ready:
        node = ready.popleft()
        result.append(node)

        for neighbor in adjacency[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                ready.append(neighbor)

    if len(result) != len(node_order):
        raise ValueError("graph contains a cycle")

    return result
