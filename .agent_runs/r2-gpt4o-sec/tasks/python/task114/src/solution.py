# src/solution.py

from collections import defaultdict, deque

def topo_sort(graph):
    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary")

    # Initialize in-degree of each node to 0
    in_degree = defaultdict(int)
    for node in graph:
        if not isinstance(node, str) or not isinstance(graph[node], list):
            raise ValueError("Graph must be a dictionary of {node: [neighbors]}")

        for neighbor in graph[node]:
            if not isinstance(neighbor, str):
                raise ValueError("Graph must be a dictionary of {node: [neighbors]}")
            in_degree[neighbor] += 1

    # Collect nodes with no incoming edges
    zero_in_degree = deque([node for node in graph if in_degree[node] == 0])

    topo_order = []
    while zero_in_degree:
        node = zero_in_degree.popleft()
        topo_order.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)

    if len(topo_order) != len(graph):
        raise ValueError("Graph has at least one cycle")

    return topo_order
