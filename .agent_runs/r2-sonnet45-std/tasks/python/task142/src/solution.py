import heapq


def dijkstra(graph, start):
    """
    Compute shortest-path distances from start to all reachable nodes using Dijkstra's algorithm.
    
    Args:
        graph: dict mapping each node to a list of (neighbor, weight) tuples
        start: starting node
        
    Returns:
        dict mapping each reachable node to its shortest distance from start
        
    Raises:
        ValueError: if start is not in graph or if any edge weight is negative
    """
    # Validate that start is in graph
    if start not in graph:
        raise ValueError(f"Start node {start} not in graph")
    
    # Validate that all edge weights are non-negative
    for node, edges in graph.items():
        for neighbor, weight in edges:
            if weight < 0:
                raise ValueError(f"Negative edge weight {weight} found")
    
    # Initialize distances
    distances = {start: 0}
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    
    # Set of visited nodes
    visited = set()
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # If current node is in graph, process its neighbors
        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                if neighbor not in visited:
                    new_dist = current_dist + weight
                    
                    # Update distance if we found a shorter path
                    if neighbor not in distances or new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor))
    
    return distances
