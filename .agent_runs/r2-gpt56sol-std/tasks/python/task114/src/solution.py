"""Topological sorting for directed graphs."""

from collections import deque
from collections.abc import Hashable, Iterable, Mapping
from typing import TypeVar

Node = TypeVar("Node", bound=Hashable)


def topo_sort(graph: Mapping[Node, Iterable[Node]]) -> list[Node]:
    """Return a topological ordering of *graph*.

    Nodes that appear only as neighbors are included in the result.

    Raises:
        ValueError: If the graph contains a directed cycle.
    """
    adjacency: dict[Node, list[Node]] = {node: [] for node in graph}
    indegree: dict[Node, int] = {node: 0 for node in graph}

    for node, neighbors in graph.items():
        edges = list(neighbors)
        adjacency[node] = edges

        for neighbor in edges:
            if neighbor not in adjacency:
                adjacency[neighbor] = []
                indegree[neighbor] = 0
            indegree[neighbor] += 1

    ready = deque(node for node in adjacency if indegree[node] == 0)
    result: list[Node] = []

    while ready:
        node = ready.popleft()
        result.append(node)

        for neighbor in adjacency[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                ready.append(neighbor)

    if len(result) != len(adjacency):
        raise ValueError("graph contains a cycle")

    return result
