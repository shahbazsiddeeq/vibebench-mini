# src/solution.py

from collections import deque
from typing import List, Dict

def bfs_shortest_path(graph: Dict[str, List[str]], start: str, end: str) -> List[str]:
    # Validate inputs
    if not isinstance(graph, dict) or not all(isinstance(k, str) and isinstance(v, list) for k, v in graph.items()):
        return []
    if not isinstance(start, str) or not isinstance(end, str):
        return []
    
    # Handle the case where start and end are the same
    if start == end:
        return [start]
    
    # Check if start and end are in the graph
    if start not in graph or end not in graph:
        return []
    
    # Initialize the queue for BFS and the visited set
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current_node, path = queue.popleft()
        
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                if neighbor == end:
                    return path + [end]
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []
