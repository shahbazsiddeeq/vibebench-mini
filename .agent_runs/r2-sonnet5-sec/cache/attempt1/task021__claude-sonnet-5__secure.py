"""
src/solution.py

Breadth-First Search shortest path utility for undirected adjacency-list
graphs.

This module intentionally avoids any use of eval/exec, external I/O, or
non-deterministic behaviour tied to insecure randomness. All inputs are
validated defensively so that malformed data structures do not raise
unexpected/internal exceptions to the caller.
"""

from collections import deque
from typing import Any, Dict, Hashable, List


def _is_valid_graph(graph: Any) -> bool:
    """
    Validate that `graph` is a mapping from hashable node identifiers to
    iterables of hashable neighbour identifiers.

    This is a defensive check to ensure we never operate on unexpected
    types (e.g. objects with malicious __iter__/__hash__ side effects are
    still subject to Python's normal semantics, but at least we guard
    against wildly incorrect shapes such as non-dict graphs or non-list
    neighbour containers).
    """
    if not isinstance(graph, dict):
        return False

    for node, neighbours in graph.items():
        if not isinstance(node, Hashable):
            return False
        if not isinstance(neighbours, (list, tuple, set)):
            return False
        for neighbour in neighbours:
            if not isinstance(neighbour, Hashable):
                return False

    return True


def bfs_shortest_path(
    graph: Dict[Hashable, List[Hashable]],
    start: Hashable,
    end: Hashable,
) -> List[Hashable]:
    """
    Return a shortest path (fewest edges) between `start` and `end` in the
    undirected adjacency-list graph `graph`, using breadth-first search.

    Parameters
    ----------
    graph : dict
        Maps each node to a list (or other iterable) of its neighbours.
    start : hashable
        The starting node.
    end : hashable
        The target node.

    Returns
    -------
    list
        A list of node names representing a shortest path from `start` to
        `end`, inclusive. If `start == end`, returns `[start]`. If no path
        exists (including cases where `start` or `end` is missing from
        `graph`), returns an empty list.
    """
    # Validate the graph shape defensively; if it's not sensible, there is
    # no safe way to traverse it, so report "no path" rather than raising.
    if not _is_valid_graph(graph):
        return []

    # Trivial case: start and end are the same node. This is valid even if
    # the node itself is not present in the graph, per the spec.
    if start == end:
        return [start]

    # If either endpoint is missing from the graph, no path can exist.
    if start not in graph or end not in graph:
        return []

    visited = {start}
    parent: Dict[Hashable, Hashable] = {}
    queue = deque([start])

    while queue:
        current = queue.popleft()

        neighbours = graph.get(current, [])
        # Guard against unexpected non-iterable values defensively even
        # though _is_valid_graph already checked this.
        try:
            neighbour_iter = list(neighbours)
        except TypeError:
            neighbour_iter = []

        for neighbour in neighbour_iter:
            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = current

            if neighbour == end:
                # Reconstruct path from end back to start.
                path = [end]
                node = end
                while node != start:
                    node = parent[node]
                    path.append(node)
                path.reverse()
                return path

            queue.append(neighbour)

    # No path found.
    return []
