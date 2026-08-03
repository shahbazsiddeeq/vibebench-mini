# src/solution.py

from collections import defaultdict, deque

def topo_sort(graph):
    # Validate input
    if not isinstance(graph, dict):
        raise ValueError("Input must be a dictionary.")
    
    for node, neighbors in graph.items():
        if not isinstance(node, str) or not isinstance(neighbors, list):
            raise ValueError("Graph must be a dictionary with string keys and list values.")
        for neighbor in neighbors:
            if not isinstance(neighbor, str):
                raise ValueError("All neighbors must be strings.")
    
    # Initialize data structures
    in_degree = {node: 0 for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            in_degree[neighbor] += 1

    # Queue for nodes with no incoming edges
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    topo_order = []

    while queue:
        current = queue.popleft()
        topo_order.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycles
    if len(topo_order) != len(graph):
        raise ValueError("Graph has at least one cycle.")

    return topo_order
