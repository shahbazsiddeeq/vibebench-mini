from collections import deque
from collections.abc import Mapping
from typing import Any


def bfs_shortest_path(graph: Mapping[Any, list[Any]], start: Any, end: Any) -> list[Any]:
    """Return a shortest path from start to end using breadth-first search."""
    try:
        if start == end:
            return [start]
    except Exception:
        return []

    if not isinstance(graph, Mapping):
        return []

    try:
        if start not in graph or end not in graph:
            return []
        hash(start)
        hash(end)
    except (KeyError, TypeError, ValueError):
        return []
    except Exception:
        return []

    queue = deque([start])
    parents: dict[Any, Any | None] = {start: None}

    while queue:
        current = queue.popleft()

        try:
            neighbours = graph.get(current, [])
        except Exception:
            return []

        if not isinstance(neighbours, (list, tuple)):
            return []

        for neighbour in neighbours:
            try:
                if neighbour in parents:
                    continue
                hash(neighbour)
            except (TypeError, ValueError):
                continue
            except Exception:
                return []

            parents[neighbour] = current

            try:
                is_end = neighbour == end
            except Exception:
                return []

            if is_end:
                path = [end]
                node = end
                while parents[node] is not None:
                    node = parents[node]
                    path.append(node)
                path.reverse()
                return path

            if neighbour in graph:
                queue.append(neighbour)

    return []
