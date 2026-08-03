import heapq
from typing import Dict, List, Tuple, Any


def dijkstra(graph: Dict[Any, List[Tuple[Any, int]]], start: Any) -> Dict[Any, int]:
    """
    Compute shortest-path distances from start node using Dijkstra's algorithm.
    
    Args:
        graph: Dictionary mapping each node to a list of (neighbor, weight) tuples.
               Weights must be non-negative integers.
        start: The starting node (must be a key in graph).
    
    Returns:
        Dictionary mapping each reachable node to its shortest distance from start.
        The start node maps to 0. Unreachable nodes are omitted.
    
    Raises:
        ValueError: If start is not a key in graph or if any edge weight is negative.
    """
    # Validate that start is in graph
    if start not in graph:
        raise ValueError("Start node is not a key in graph")
    
    # Validate graph structure and edge weights
    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary")
    
    for node, edges in graph.items():
        if not isinstance(edges, list):
            raise ValueError("Each node must map to a list of edges")
        
        for edge in edges:
            if not isinstance(edge, tuple) or len(edge) != 2:
                raise ValueError("Each edge must be a (neighbor, weight) tuple")
            
            neighbor, weight = edge
            
            # Validate weight is non-negative integer
            if not isinstance(weight, int):
                raise ValueError("Edge weights must be integers")
            if weight < 0:
                raise ValueError("Edge weights must be non-negative")
    
    # Initialize distances dictionary
    distances = {start: 0}
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    
    # Set to track visited nodes
    visited = set()
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # Skip if this is an outdated entry
        if current_dist > distances.get(current_node, float('inf')):
            continue
        
        # Process neighbors if current_node is in graph
        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                new_dist = current_dist + weight
                
                # Update distance if we found a shorter path
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))
    
    return distances
