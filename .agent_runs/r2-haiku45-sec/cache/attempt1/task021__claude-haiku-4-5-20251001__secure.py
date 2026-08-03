"""
BFS Shortest Path implementation.

This module provides a breadth-first search algorithm to find the shortest path
between two nodes in an undirected adjacency-list graph.
"""

from collections import deque
from typing import Dict, List, Any


def bfs_shortest_path(
    graph: Dict[str, List[str]], start: str, end: str
) -> List[str]:
    """
    Find the shortest path between two nodes in an undirected graph using BFS.
    
    Args:
        graph: An adjacency-list representation where keys are node names
               and values are lists of neighboring node names.
        start: The starting node name.
        end: The ending node name.
    
    Returns:
        A list of node names representing the shortest path from start to end.
        Returns [start] if start == end.
        Returns [] if no path exists or if start/end are not in the graph
        (except when start == end).
    
    Raises:
        TypeError: If graph is not a dict, or start/end are not strings.
    """
    # Input validation
    if not isinstance(graph, dict):
        raise TypeError("graph must be a dictionary")
    if not isinstance(start, str):
        raise TypeError("start must be a string")
    if not isinstance(end, str):
        raise TypeError("end must be a string")
    
    # Validate graph structure
    for node, neighbors in graph.items():
        if not isinstance(node, str):
            raise TypeError("all graph keys must be strings")
        if not isinstance(neighbors, list):
            raise TypeError("all graph values must be lists")
        for neighbor in neighbors:
            if not isinstance(neighbor, str):
                raise TypeError("all neighbors must be strings")
    
    # Handle case where start equals end
    if start == end:
        return [start]
    
    # If start or end is not in the graph, no path exists
    if start not in graph or end not in graph:
        return []
    
    # BFS to find shortest path
    queue: deque = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current_node, path = queue.popleft()
        
        # Check neighbors of current node
        neighbors = graph.get(current_node, [])
        for neighbor in neighbors:
            if neighbor == end:
                # Found the destination
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    # No path found
    return []
