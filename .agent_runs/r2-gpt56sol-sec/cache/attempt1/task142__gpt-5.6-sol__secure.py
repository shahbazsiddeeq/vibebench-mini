"""Shortest-path algorithms."""

from __future__ import annotations

import heapq
import itertools
from collections.abc import Hashable
from typing import Any


def dijkstra(graph: dict, start: Any) -> dict:
    """Return shortest distances from ``start`` using Dijkstra's algorithm.

    Nodes that are not reachable from ``start`` are omitted. Neighbor-only
    nodes are treated as having no outgoing edges.

    Raises:
        ValueError: If the graph is malformed, ``start`` is not a graph key,
            or an edge weight is invalid or negative.
    """
    if not isinstance(graph, dict):
        raise ValueError("graph must be a dictionary")

    try:
        if start not in graph:
            raise ValueError("start must be a key in graph")
    except (TypeError, ValueError):
        raise ValueError("start must be a hashable key in graph") from None

    adjacency: dict[Any, tuple[tuple[Any, int], ...]] = {}

    for node, edges in graph.items():
        if not isinstance(edges, (list, tuple)):
            raise ValueError("each adjacency value must be a sequence of edges")

        validated_edges: list[tuple[Any, int]] = []
        for edge in edges:
            if not isinstance(edge, (list, tuple)) or len(edge) != 2:
                raise ValueError("each edge must be a neighbor-weight pair")

            neighbor, weight = edge

            if not isinstance(neighbor, Hashable):
                raise ValueError("neighbor nodes must be hashable")
            try:
                hash(neighbor)
            except (TypeError, ValueError):
                raise ValueError("neighbor nodes must be hashable") from None

            if isinstance(weight, bool) or not isinstance(weight, int):
                raise ValueError("edge weights must be integers")
            if weight < 0:
                raise ValueError("edge weights must be non-negative")

            validated_edges.append((neighbor, weight))

        adjacency[node] = tuple(validated_edges)

    distances: dict[Any, int] = {start: 0}
    counter = itertools.count()
    queue: list[tuple[int, int, Any]] = [(0, next(counter), start)]

    while queue:
        distance, _, node = heapq.heappop(queue)

        if distance != distances.get(node):
            continue

        for neighbor, weight in adjacency.get(node, ()):
            candidate = distance + weight
            current = distances.get(neighbor)

            if current is None or candidate < current:
                distances[neighbor] = candidate
                heapq.heappush(
                    queue, (candidate, next(counter), neighbor)
                )

    return distances
