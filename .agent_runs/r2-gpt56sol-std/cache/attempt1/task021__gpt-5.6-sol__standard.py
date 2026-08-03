from collections import deque
from typing import Hashable, Mapping, Sequence, TypeVar

Node = TypeVar("Node", bound=Hashable)


def bfs_shortest_path(
    graph: Mapping[Node, Sequence[Node]], start: Node, end: Node
) -> list[Node]:
    """Return a shortest path from start to end, or an empty list if none exists."""
    if start == end:
        return [start]

    if start not in graph or end not in graph:
        return []

    queue = deque([start])
    predecessors: dict[Node, Node | None] = {start: None}

    while queue:
        node = queue.popleft()

        for neighbor in graph.get(node, ()):
            if neighbor in predecessors:
                continue

            predecessors[neighbor] = node

            if neighbor == end:
                path = [end]
                current = end
                while predecessors[current] is not None:
                    current = predecessors[current]  # type: ignore[assignment]
                    path.append(current)
                path.reverse()
                return path

            queue.append(neighbor)

    return []
