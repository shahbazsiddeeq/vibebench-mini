def topo_sort(graph):
    """
    Performs a topological sort on a directed graph.

    Args:
        graph (dict): A dictionary representing the graph where keys are nodes
                      and values are lists of their neighbors.

    Returns:
        list: A list of nodes in topological order.

    Raises:
        ValueError: If a cycle is detected in the graph or if the input graph
                    is invalid (e.g., contains non-string/non-integer nodes,
                    or non-list neighbors).
    """
    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary.")

    # Validate graph structure and nodes
    nodes = set()
    for node, neighbors in graph.items():
        if not isinstance(node, (str, int)):
            raise ValueError(f"Invalid node type: {type(node)}. Nodes must be strings or integers.")
        nodes.add(node)
        if not isinstance(neighbors, list):
            raise ValueError(f"Neighbors of node '{node}' must be a list.")
        for neighbor in neighbors:
            if not isinstance(neighbor, (str, int)):
                raise ValueError(f"Invalid neighbor type: {type(neighbor)}. Neighbors must be strings or integers.")
            nodes.add(neighbor)

    # Calculate in-degrees for all nodes
    in_degree = {node: 0 for node in nodes}
    for node in graph:
        for neighbor in graph[node]:
            if neighbor not in in_degree:
                # This case should ideally be caught by the initial node validation,
                # but as a safeguard, ensure all referenced nodes are in in_degree.
                in_degree[neighbor] = 0
            in_degree[neighbor] += 1

    # Initialize queue with nodes having an in-degree of 0
    queue = [node for node in nodes if in_degree[node] == 0]
    
    # If there are nodes in the graph that are not keys in the graph dict
    # but are referenced as neighbors, they might not be in the initial queue
    # if they have an in-degree of 0. Ensure they are added.
    for node in nodes:
        if node not in graph and in_degree[node] == 0 and node not in queue:
            queue.append(node)

    topological_order = []
    visited_count = 0

    while queue:
        current_node = queue.pop(0)
        topological_order.append(current_node)
        visited_count += 1

        # Only process neighbors if the current_node is a key in the graph
        if current_node in graph:
            for neighbor in graph[current_node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    if visited_count != len(nodes):
        raise ValueError("Cycle detected in the graph.")

    return topological_order
