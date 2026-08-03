#!/usr/bin/env python3
"""Create a public/hidden test split for every CodeAssay Python task.

For each tasks/python/task*/tests/test_solution.py:
  - keep the module preamble (imports, helpers, fixtures, classes, constants)
    in BOTH outputs;
  - partition the top-level `def test_*` functions ~50/50, interleaved by index
    (even index -> hidden, odd index -> public) so each side gets a spread of
    early (canonical) and later (edge-case) tests;
  - write tests_public/test_solution.py  (shown to the model + used for repair)
          tests_hidden/test_solution.py  (grading only).

The original tests/ directory is left untouched (additive, reversible).
Writes tasks/python/test_split_manifest.json with per-task details.
Deletes nothing. Idempotent: re-running overwrites the two generated files.

Usage: python scripts/make_test_split.py            # all tasks
       python scripts/make_test_split.py --check     # also ast-validate outputs
"""
import ast
import glob
import json
import os
import sys

ROOT = "tasks/python"


def func_span(node):
    """First..last source line (1-based, inclusive) of a def, incl. decorators."""
    start = node.lineno
    for d in getattr(node, "decorator_list", []):
        start = min(start, d.lineno)
    return start, node.end_lineno


def split_source(src):
    tree = ast.parse(src)
    lines = src.splitlines()
    test_funcs = [
        n for n in tree.body
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        and n.name.startswith("test")
    ]
    has_class = any(isinstance(n, ast.ClassDef) for n in tree.body)

    # lines occupied by test functions (to exclude from preamble)
    tf_lines = set()
    spans = []
    for n in test_funcs:
        s, e = func_span(n)
        spans.append((s, e, n.name))
        for ln in range(s - 1, e):
            tf_lines.add(ln)
    preamble = "\n".join(
        lines[i] for i in range(len(lines)) if i not in tf_lines
    ).strip()

    def text(span):
        s, e, _ = span
        return "\n".join(lines[s - 1:e])

    hidden_spans = [sp for i, sp in enumerate(spans) if i % 2 == 0]  # even -> hidden (ceil)
    public_spans = [sp for i, sp in enumerate(spans) if i % 2 == 1]  # odd  -> public

    def build(chosen):
        body = "\n\n\n".join(text(sp) for sp in chosen)
        return (preamble + "\n\n\n" + body).strip() + "\n"

    return {
        "n_total": len(spans),
        "public": build(public_spans),
        "hidden": build(hidden_spans),
        "public_names": [sp[2] for sp in public_spans],
        "hidden_names": [sp[2] for sp in hidden_spans],
        "has_class": has_class,
    }


def main():
    check = "--check" in sys.argv
    files = sorted(glob.glob(os.path.join(ROOT, "task*/tests/test_solution.py")))
    manifest = {}
    errors = []
    for f in files:
        task = f.split("/")[2]
        src = open(f, encoding="utf-8").read()
        try:
            r = split_source(src)
        except Exception as e:  # noqa
            errors.append((task, repr(e)))
            continue
        if not r["public_names"] or not r["hidden_names"]:
            errors.append((task, "empty public or hidden after split"))
            continue
        tdir = os.path.dirname(os.path.dirname(f))
        for sub, key in (("tests_public", "public"), ("tests_hidden", "hidden")):
            d = os.path.join(tdir, sub)
            os.makedirs(d, exist_ok=True)
            out = os.path.join(d, "test_solution.py")
            open(out, "w", encoding="utf-8").write(r[key])
            if check:
                ast.parse(open(out, encoding="utf-8").read())  # validate
        manifest[task] = {
            "n_total": r["n_total"],
            "n_public": len(r["public_names"]),
            "n_hidden": len(r["hidden_names"]),
            "public_names": r["public_names"],
            "hidden_names": r["hidden_names"],
            "has_class": r["has_class"],
        }
    mpath = os.path.join(ROOT, "test_split_manifest.json")
    json.dump(manifest, open(mpath, "w", encoding="utf-8"), indent=2)

    n = len(manifest)
    tot = sum(m["n_total"] for m in manifest.values())
    pub = sum(m["n_public"] for m in manifest.values())
    hid = sum(m["n_hidden"] for m in manifest.values())
    cls = [t for t, m in manifest.items() if m["has_class"]]
    print(f"tasks split: {n}/{len(files)}")
    print(f"test functions: total={tot}  public={pub}  hidden={hid}")
    print(f"class-based tasks (review): {cls}")
    print(f"manifest: {mpath}")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for t, e in errors:
            print("  ", t, e)
        sys.exit(1)


if __name__ == "__main__":
    main()
