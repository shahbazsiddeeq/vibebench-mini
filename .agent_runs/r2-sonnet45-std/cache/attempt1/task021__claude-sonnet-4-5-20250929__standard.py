from collections import deque

def bfs_shortest_path(graph, start, end):
    """
    Find shortest path between start and end nodes using BFS.
    
    Args:
        graph: dict mapping each node to a list of its neighbors
        start: starting node
        end: ending node
    
    Returns:
        List of nodes representing the shortest path, or [] if no path exists
    """
    # Handle the case where start equals end
    if start == end:
        return [start]
    
    # If start or end is not in graph, no path can be found
    if start not in graph or end not in graph:
        return []
    
    # BFS setup
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    # Perform BFS
    while queue:
        current = queue.popleft()
        
        # Check neighbors
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                
                # If we found the end node, reconstruct the path
                if neighbor == end:
                    path = []
                    node = end
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    return path[::-1]  # Reverse to get start -> end
    
    # No path found
    return []
