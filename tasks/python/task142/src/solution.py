from __future__ import annotations

import heapq
from typing import Any


def dijkstra(graph: dict, start: Any) -> dict:
    """Return shortest-path distances from ``start`` to every reachable node."""
    if start not in graph:
        raise ValueError("start must be a key in graph")

    dist: dict = {start: 0}
    heap: list[tuple[int, int, Any]] = [(0, 0, start)]
    counter = 1  # tie-breaker so heap never compares node objects

    while heap:
        d, _, node = heapq.heappop(heap)
        if d > dist.get(node, float("inf")):
            continue
        for neighbor, weight in graph.get(node, []):
            if weight < 0:
                raise ValueError("edge weights must be non-negative")
            nd = d + weight
            if nd < dist.get(neighbor, float("inf")):
                dist[neighbor] = nd
                heapq.heappush(heap, (nd, counter, neighbor))
                counter += 1

    return dist
