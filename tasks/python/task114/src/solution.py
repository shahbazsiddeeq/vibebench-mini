def topo_sort(graph: dict[str, list[str]]) -> list[str]:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    result = []

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if neighbor not in color:
                color[neighbor] = WHITE
            if color[neighbor] == GRAY:
                raise ValueError("Graph has a cycle")
            if color[neighbor] == WHITE:
                dfs(neighbor)
        color[node] = BLACK
        result.append(node)

    for node in graph:
        if color[node] == WHITE:
            dfs(node)

    return list(reversed(result))
