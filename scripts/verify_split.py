#!/usr/bin/env python3
"""Verify the public/hidden split: the reference solution must pass BOTH subsets
for every task. Writes a JSON report and prints a summary.

Run: python scripts/verify_split.py
"""
import glob
import json
import os
import shutil
import subprocess
import sys

PYTEST = shutil.which("pytest") or "pytest"
tasks = sorted(glob.glob("tasks/python/task*/"))
tasks = [t for t in tasks if os.path.isdir(os.path.join(t, "tests_hidden"))]


def run(tdir, sub):
    env = dict(os.environ, PYTHONPATH=".")
    try:
        p = subprocess.run(
            [PYTEST, "-q", "--no-header", "-p", "no:cacheprovider", sub],
            cwd=tdir, capture_output=True, text=True, timeout=180, env=env,
        )
        last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr.strip()[-160:]
        return p.returncode == 0, last
    except Exception as e:  # noqa
        return False, repr(e)[:160]


report = {}
pub_fail, hid_fail = [], []
for t in tasks:
    name = os.path.basename(t.rstrip("/"))
    okp, lp = run(t, "tests_public")
    okh, lh = run(t, "tests_hidden")
    report[name] = {"public_ok": okp, "hidden_ok": okh, "public_last": lp, "hidden_last": lh}
    if not okp:
        pub_fail.append(name)
    if not okh:
        hid_fail.append(name)

out = "tasks/python/test_split_verify.json"
json.dump(report, open(out, "w"), indent=2)
n = len(tasks)
print(f"verified {n} tasks")
print(f"public PASS: {n - len(pub_fail)}/{n}  fails: {pub_fail}")
print(f"hidden PASS: {n - len(hid_fail)}/{n}  fails: {hid_fail}")
print(f"report: {out}")
sys.exit(0 if not (pub_fail or hid_fail) else 1)
