def topo_sort(graph):
    from collections import defaultdict, deque

    # Calculate in-degrees of all nodes
    in_degree = defaultdict(int)
    for node in graph:
        in_degree[node] = 0
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Collect nodes with zero in-degree
    zero_in_degree = deque([node for node in graph if in_degree[node] == 0])

    topo_order = []
    while zero_in_degree:
        node = zero_in_degree.popleft()
        topo_order.append(node)

        # Decrease in-degree of neighbors
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)

    # If topo_order contains all nodes, return it; otherwise, a cycle exists
    if len(topo_order) == len(graph):
        return topo_order
    else:
        raise ValueError("Graph contains a cycle")
