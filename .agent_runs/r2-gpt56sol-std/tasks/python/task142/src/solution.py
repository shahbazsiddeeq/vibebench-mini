"""Shortest-path algorithms."""

from heapq import heappop, heappush
from itertools import count
from typing import Any


def dijkstra(graph: dict, start: Any) -> dict:
    """Return shortest-path distances from ``start`` using Dijkstra's algorithm.

    Nodes that are not reachable from ``start`` are omitted. Nodes appearing
    only as edge destinations are treated as having no outgoing edges.

    Raises:
        ValueError: If ``start`` is not a key in ``graph`` or any edge has a
            negative weight.
    """
    if start not in graph:
        raise ValueError("start node is not in graph")

    for edges in graph.values():
        for _, weight in edges:
            if weight < 0:
                raise ValueError("Dijkstra's algorithm requires non-negative weights")

    distances = {start: 0}
    tie_breaker = count()
    queue = [(0, next(tie_breaker), start)]

    while queue:
        distance, _, node = heappop(queue)

        if distance != distances.get(node):
            continue

        for neighbor, weight in graph.get(node, ()):
            candidate = distance + weight
            if neighbor not in distances or candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heappush(queue, (candidate, next(tie_breaker), neighbor))

    return distances
