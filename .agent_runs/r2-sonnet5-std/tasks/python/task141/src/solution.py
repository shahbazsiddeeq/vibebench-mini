def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    if n < 0:
        raise ValueError("n must be non-negative")

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    for u, v in edges:
        if u not in range(n) or v not in range(n):
            raise ValueError(f"edge endpoint out of range: ({u}, {v})")
        union(u, v)

    groups: dict[int, list[int]] = {}
    for node in range(n):
        root = find(node)
        groups.setdefault(root, []).append(node)

    components = sorted(groups.values(), key=lambda comp: comp[0])
    return components
