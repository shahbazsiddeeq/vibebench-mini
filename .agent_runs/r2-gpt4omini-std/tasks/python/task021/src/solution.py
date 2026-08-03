# src/solution.py

from collections import deque

def bfs_shortest_path(graph, start, end):
    if start == end:
        return [start]
    
    if start not in graph or end not in graph:
        return []
    
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        current_node, path = queue.popleft()
        
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                if neighbor == end:
                    return path + [neighbor]
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []
