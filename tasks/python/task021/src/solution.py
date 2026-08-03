from __future__ import annotations

from collections import deque


def bfs_shortest_path(graph: dict[str, list[str]], start: str, end: str) -> list[str]:
    if start == end:
        return [start]
    visited = {start}
    queue: deque[list[str]] = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        for neighbour in graph.get(node, []):
            if neighbour == end:
                return path + [neighbour]
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(path + [neighbour])
    return []
