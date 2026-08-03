"""BFS Shortest Path module."""
from collections import deque


def bfs_shortest_path(graph, start, end):
    """
    Return a shortest path (fewest edges) between start and end in an
    undirected adjacency-list graph, using breadth-first search.

    Args:
        graph: dict mapping node -> list of neighbouring nodes.
        start: starting node.
        end: target node.

    Returns:
        List of nodes representing a shortest path from start to end,
        inclusive. If start == end, returns [start]. If no path exists,
        returns [].
    """
    if start == end:
        return [start]

    if start not in graph or end not in graph:
        return []

    visited = {start}
    queue = deque([start])
    parent = {}

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if end not in visited:
        return []

    path = [end]
    node = end
    while node != start:
        node = parent[node]
        path.append(node)
    path.reverse()
    return path
