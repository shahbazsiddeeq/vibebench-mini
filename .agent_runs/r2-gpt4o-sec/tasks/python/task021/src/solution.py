from collections import deque
from typing import Dict, List

def bfs_shortest_path(graph: Dict[str, List[str]], start: str, end: str) -> List[str]:
    if start == end:
        return [start]
    
    if start not in graph or end not in graph:
        return []
    
    visited = set()
    queue = deque([[start]])
    
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
