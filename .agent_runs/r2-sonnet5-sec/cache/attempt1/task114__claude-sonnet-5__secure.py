"""Topological sort implementation.

This module provides a single public function, ``topo_sort``, which computes
a topological ordering of the nodes of a directed graph represented as an
adjacency mapping ``{node: [neighbors, ...]}``.

The implementation favours safety and correctness:

* All inputs are validated before any processing occurs.
* No use of ``eval``/``exec`` or other unsafe constructs.
* Errors are raised using generic, non-leaky messages (no internal state,
  file paths, or stack traces are exposed to callers).
* The algorithm (Kahn's algorithm) is deterministic and runs in O(V + E).
"""

from collections import deque
from typing import Dict, Hashable, List, Sequence


def _validate_graph(graph: Dict[Hashable, Sequence[Hashable]]) -> None:
    """Validate the structure of the input graph.

    Raises:
        TypeError: if the graph or its components are not of the expected
            type.
        ValueError: if the graph references neighbors that are not declared
            as nodes.
    """
    if not isinstance(graph, dict):
        raise TypeError("graph must be a dictionary")

    for node, neighbors in graph.items():
        if not isinstance(node, Hashable):
            raise TypeError("graph node keys must be hashable")
        if isinstance(neighbors, (str, bytes)) or not isinstance(neighbors, (list, tuple, set)):
            raise TypeError("adjacency list values must be a list, tuple, or set of nodes")

    all_nodes = set(graph.keys())
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor not in all_nodes:
                raise ValueError("graph contains an edge to an undeclared node")


def topo_sort(graph: Dict[Hashable, Sequence[Hashable]]) -> List[Hashable]:
    """Compute a topological ordering of the given directed graph.

    Args:
        graph: A mapping of node -> iterable of neighbor nodes representing
            directed edges (node -> neighbor).

    Returns:
        A list of nodes in a valid topological order.

    Raises:
        TypeError: if the input is not a properly structured graph.
        ValueError: if the graph contains a cycle, or references undeclared
            nodes.
    """
    _validate_graph(graph)

    # Compute in-degrees for all nodes.
    in_degree: Dict[Hashable, int] = {node: 0 for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            in_degree[neighbor] += 1

    # Initialize queue with nodes that have zero in-degree.
    # Use insertion order of the original dict for determinism.
    queue = deque(node for node in graph if in_degree[node] == 0)

    result: List[Hashable] = []

    while queue:
        current = queue.popleft()
        result.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(graph):
        raise ValueError("graph contains a cycle; topological sort is not possible")

    return result
