from collections import deque

def bfs_shortest_path(graph, start, end):
    """
    Find the shortest path between start and end nodes in an undirected graph
    using breadth-first search.
    
    Args:
        graph: Dictionary mapping node names to lists of neighbors
        start: Starting node name
        end: Ending node name
    
    Returns:
        List of node names representing the shortest path from start to end.
        Returns [start] if start == end.
        Returns [] if no path exists or if start/end not in graph (when start != end).
    """
    # If start equals end, return [start]
    if start == end:
        return [start]
    
    # If start or end is not in the graph, no path can be found
    if start not in graph or end not in graph:
        return []
    
    # BFS to find shortest path
    queue = deque([(start, [start])])  # (current_node, path_to_current_node)
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        # Explore neighbors
        for neighbor in graph.get(current, []):
            if neighbor == end:
                # Found the end node
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    # No path found
    return []
