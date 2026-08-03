# src/solution.py

def topo_sort(graph):
    from collections import defaultdict, deque

    # Step 1: Calculate in-degrees
    in_degree = {node: 0 for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            in_degree[neighbor] += 1

    # Step 2: Initialize the queue with nodes having in-degree of 0
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    topological_order = []

    # Step 3: Process the nodes
    while queue:
        node = queue.popleft()
        topological_order.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Step 4: Check for cycles
    if len(topological_order) != len(graph):
        raise ValueError("Graph has at least one cycle")

    return topological_order
