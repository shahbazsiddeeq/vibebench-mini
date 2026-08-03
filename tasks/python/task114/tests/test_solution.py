import pytest
from src.solution import topo_sort


def test_linear():
    result = topo_sort({"a": ["b"], "b": ["c"], "c": []})
    assert result.index("a") < result.index("b") < result.index("c")


def test_cycle():
    with pytest.raises(ValueError):
        topo_sort({"a": ["b"], "b": ["a"]})


def test_no_deps():
    result = topo_sort({"a": [], "b": [], "c": []})
    assert set(result) == {"a", "b", "c"}


def test_diamond():
    g = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    result = topo_sort(g)
    assert result.index("a") < result.index("d")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")


def test_key_order_violates_topological_order():
    # Dict key order (c, b, a) is the reverse of a valid ordering, so an
    # implementation that just returns list(graph) would fail this.
    g = {"c": [], "b": ["c"], "a": ["b"]}
    result = topo_sort(g)
    assert set(result) == {"a", "b", "c"}
    assert result.index("a") < result.index("b") < result.index("c")


def test_returns_all_nodes():
    g = {"x": ["y"], "y": ["z"], "z": [], "w": ["x"]}
    result = topo_sort(g)
    assert set(result) == {"w", "x", "y", "z"}
    assert len(result) == 4
    assert result.index("w") < result.index("x") < result.index("y") < result.index("z")
