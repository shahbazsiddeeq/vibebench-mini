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
        raise ValueError("Number of nodes must be non-negative.")
    
    uf = UnionFind(n)

    for u, v in edges:
        if not (0 <= u < n) or not (0 <= v < n):
            raise ValueError("Edge endpoints must be in range [0, n-1].")
        uf.union(u, v)

    components = {}
    for node in range(n):
        root = uf.find(node)
        if root not in components:
            components[root] = []
        components[root].append(node)

    # Sort each component and the list of components
    result = [sorted(component) for component in components.values()]
    return sorted(result, key=lambda x: x[0])
