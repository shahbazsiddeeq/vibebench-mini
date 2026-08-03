class UnionFind:
    """
    A Union-Find data structure for tracking connected components.
    """

    def __init__(self, n: int):
        """
        Initializes the Union-Find structure with n elements.
        Each element is initially in its own set.

        Args:
            n: The number of elements.
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a non-negative integer.")
        self._parent = list(range(n))
        self._size = [1] * n

    def find(self, i: int) -> int:
        """
        Finds the representative (root) of the set containing element i.
        Performs path compression for efficiency.

        Args:
            i: The element to find the representative for.

        Returns:
            The representative of the set containing i.
        """
        if not isinstance(i, int) or not (0 <= i < len(self._parent)):
            raise ValueError(f"Node {i} is out of bounds.")

        if self._parent[i] == i:
            return i
        self._parent[i] = self.find(self._parent[i])
        return self._parent[i]

    def union(self, i: int, j: int) -> None:
        """
        Unites the sets containing elements i and j.
        Performs union by size for efficiency.

        Args:
            i: The first element.
            j: The second element.
        """
        if not isinstance(i, int) or not (0 <= i < len(self._parent)):
            raise ValueError(f"Node {i} is out of bounds.")
        if not isinstance(j, int) or not (0 <= j < len(self._parent)):
            raise ValueError(f"Node {j} is out of bounds.")

        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by size: attach smaller tree under root of larger tree
            if self._size[root_i] < self._size[root_j]:
                self._parent[root_i] = root_j
                self._size[root_j] += self._size[root_i]
            else:
                self._parent[root_j] = root_i
                self._size[root_i] += self._size[root_j]

    def get_components(self) -> dict[int, list[int]]:
        """
        Returns a dictionary where keys are component representatives
        and values are lists of nodes belonging to that component.
        """
        components = {}
        for i in range(len(self._parent)):
            root = self.find(i)
            if root not in components:
                components[root] = []
            components[root].append(i)
        return components


def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """
    Finds the connected components of an undirected graph using the Union-Find algorithm.

    Args:
        n: The number of nodes in the graph (labeled 0 to n-1).
        edges: A list of tuples, where each tuple (u, v) represents an edge
               between nodes u and v. Self-loops and duplicate edges are handled.

    Returns:
        A list of lists, where each inner list represents a connected component.
        Each component is a sorted list of its node labels, and the outer list
        is sorted by each component's smallest label.

    Raises:
        ValueError: If n is negative, or if any edge endpoint is out of the
                    range [0, n-1].
    """
    if not isinstance(n, int):
        raise ValueError("n must be an integer.")
    if n < 0:
        raise ValueError("n cannot be negative.")
    if not isinstance(edges, list):
        raise ValueError("edges must be a list.")

    uf = UnionFind(n)

    for i, edge in enumerate(edges):
        if not isinstance(edge, tuple) or len(edge) != 2:
            raise ValueError(f"Edge at index {i} is not a valid tuple (u, v).")
        u, v = edge
        if not isinstance(u, int) or not isinstance(v, int):
            raise ValueError(f"Edge endpoints at index {i} must be integers.")
        if not (0 <= u < n):
            raise ValueError(f"Edge endpoint {u} at index {i} is out of range [0, {n-1}].")
        if not (0 <= v < n):
            raise ValueError(f"Edge endpoint {v} at index {i} is out of range [0, {n-1}].")
        uf.union(u, v)

    # Collect components
    components_map = uf.get_components()

    # Sort nodes within each component and then sort components by their smallest node
    result = []
    for component_nodes in components_map.values():
        component_nodes.sort()
        result.append(component_nodes)

    # Sort the list of components based on their first element (smallest node)
    result.sort(key=lambda x: x[0])

    return result
