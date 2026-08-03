from __future__ import annotations


def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Return connected components of an undirected graph on nodes 0..n-1."""
    if n < 0:
        raise ValueError("n must be non-negative")

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        # Path compression.
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    for a, b in edges:
        if not (0 <= a < n) or not (0 <= b < n):
            raise ValueError(f"edge endpoint out of range: {(a, b)}")
        union(a, b)

    groups: dict[int, list[int]] = {}
    for node in range(n):
        groups.setdefault(find(node), []).append(node)

    components = [sorted(members) for members in groups.values()]
    components.sort(key=lambda comp: comp[0])
    return components
