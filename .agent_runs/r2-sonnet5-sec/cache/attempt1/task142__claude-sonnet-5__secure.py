"""
src/solution.py

Secure, self-contained implementation of Dijkstra's shortest path algorithm.

Design notes on security / robustness:
- Only standard library modules are used (heapq).
- All external inputs (graph, start) are validated before use.
- No eval/exec or dynamic code execution of any kind.
- No randomness is required for this task, so `secrets` is not used, but
  no insecure randomness (e.g. `random`) is used either.
- Errors raised are generic ValueError instances with safe, non-sensitive
  messages that do not leak internal state or stack details.
"""

import heapq
from typing import Any, Dict, Hashable, List, Tuple


def _validate_graph(graph: Any) -> None:
    """Validate the overall structure of the graph without leaking internals."""
    if not isinstance(graph, dict):
        raise ValueError("graph must be a dict mapping nodes to adjacency lists")

    for node, edges in graph.items():
        if not isinstance(edges, list):
            raise ValueError("adjacency list for each node must be a list")
        for edge in edges:
            if (
                not isinstance(edge, tuple)
                or len(edge) != 2
            ):
                raise ValueError("each edge must be a (neighbor, weight) tuple")
            _, weight = edge
            if not isinstance(weight, (int, float)) or isinstance(weight, bool):
                raise ValueError("edge weights must be numeric")
            if weight < 0:
                raise ValueError("edge weights must be non-negative")


def dijkstra(graph: Dict[Hashable, List[Tuple[Hashable, float]]], start: Hashable) -> Dict[Hashable, float]:
    """
    Compute shortest-path distances from `start` to every reachable node in `graph`
    using Dijkstra's algorithm.

    Parameters
    ----------
    graph : dict
        Maps each node to a list of (neighbor, weight) tuples. Weights must be
        non-negative numbers. A node that only appears as a neighbor (i.e. is
        not itself a key) is treated as having no outgoing edges.
    start : hashable
        The starting node; must be a key in `graph`.

    Returns
    -------
    dict
        Mapping of node -> shortest distance from `start`. `start` maps to 0.
        Unreachable nodes are omitted.

    Raises
    ------
    ValueError
        If `start` is not a key in `graph`, or if the graph structure is
        invalid, or if any edge weight is negative.
    """
    _validate_graph(graph)

    if start not in graph:
        raise ValueError("start node is not present in graph")

    distances: Dict[Hashable, float] = {start: 0}
    visited = set()
    # Priority queue of (distance, node)
    pq: List[Tuple[float, Hashable]] = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        # Neighbors: node may or may not have outgoing edges defined.
        neighbors = graph.get(current_node, [])

        for neighbor, weight in neighbors:
            if neighbor in visited:
                continue
            new_dist = current_dist + weight
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return distances
