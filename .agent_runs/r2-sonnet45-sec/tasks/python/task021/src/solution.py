from collections import deque
from typing import Dict, List, Any, Optional


def bfs_shortest_path(graph: Dict[str, List[str]], start: str, end: str) -> List[str]:
    """
    Find shortest path between start and end nodes using BFS.
    
    Args:
        graph: Adjacency list mapping node names to lists of neighbor names
        start: Starting node name
        end: Ending node name
    
    Returns:
        List of node names representing shortest path, or empty list if no path exists
    """
    # Input validation
    if not isinstance(graph, dict):
        return []
    
    if not isinstance(start, str) or not isinstance(end, str):
        return []
    
    # Special case: start equals end
    if start == end:
        return [start]
    
    # If start node not in graph (and start != end), no path possible
    if start not in graph:
        return []
    
    # If end node not in graph (and start != end), no path possible
    if end not in graph:
        return []
    
    # BFS setup
    queue = deque([(start, [start])])  # (current_node, path_to_current)
    visited = {start}
    
    while queue:
        current_node, path = queue.popleft()
        
        # Get neighbors safely
        neighbors = graph.get(current_node, [])
        
        # Validate neighbors is a list
        if not isinstance(neighbors, list):
            continue
        
        for neighbor in neighbors:
            # Validate neighbor is a string
            if not isinstance(neighbor, str):
                continue
            
            # Skip if already visited
            if neighbor in visited:
                continue
            
            # Mark as visited
            visited.add(neighbor)
            
            # Build new path
            new_path = path + [neighbor]
            
            # Check if we reached the end
            if neighbor == end:
                return new_path
            
            # Add to queue for further exploration
            queue.append((neighbor, new_path))
    
    # No path found
    return []
