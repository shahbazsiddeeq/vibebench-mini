# src/solution.py

from collections import deque

def bfs_shortest_path(graph, start, end):
    if start == end:
        return [start]
    
    if start not in graph or end not in graph:
        return []
    
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return []
