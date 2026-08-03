import heapq


def dijkstra(graph: dict, start) -> dict:
    if start not in graph:
        raise ValueError(f"start node {start!r} not in graph")

    for node, edges in graph.items():
        for _, weight in edges:
            if weight < 0:
                raise ValueError(f"negative edge weight found: {weight}")

    dist = {start: 0}
    visited = set()
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        for v, w in graph.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist
