# src/solution.py

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, p):
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])  # Path compression
        return self.parent[p]

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP != rootQ:
            # Union by rank
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            elif self.rank[rootP] < self.rank[rootQ]:
                self.parent[rootP] = rootQ
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1

def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    if n < 0:
        raise ValueError("n must be non-negative")
    
    uf = UnionFind(n)

    for u, v in edges:
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError("Edge endpoints must be in range(n)")
        uf.union(u, v)

    components = {}
    for i in range(n):
        root = uf.find(i)
        if root not in components:
            components[root] = []
        components[root].append(i)

    # Sort each component and the list of components
    return sorted([sorted(component) for component in components.values()], key=lambda x: x[0])
