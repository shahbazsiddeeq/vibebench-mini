#!/usr/bin/env python3
import pathlib as p

ROOT = p.Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks" / "js"
TASKS.mkdir(parents=True, exist_ok=True)

cases = [
    ("task01", "sum(a,b)", "Implement sum(a,b) returning a+b."),
    ("task02", "reverseWords(s)", "Reverse words in a string; keep single spaces."),
    ("task03", "isPalindrome(s)", "Alphanumeric, case-insensitive palindrome."),
    ("task04", "uniq(arr)", "Return array with duplicates removed, preserve order."),
    ("task05", "freqMap(arr)", "Return a Map of element -> count."),
]

for tid, sig, desc in cases:
    d = TASKS / tid
    (d / "src").mkdir(parents=True, exist_ok=True)
    (d / "tests").mkdir(parents=True, exist_ok=True)

    (d / "task.yaml").write_text(
        f"title: {sig}\ndescription: {desc}\ntrack: js\n", encoding="utf-8"
    )
    if tid == "task01":
        (d / "src" / "solution.js").write_text(
            "export function sum(a, b) {\n  return a + b;\n}\n", encoding="utf-8"
        )
        (d / "tests" / "test_solution.test.js").write_text(
            'import { describe, it, expect } from "vitest";\n'
            'import { sum } from "../src/solution.js";\n'
            "describe('sum', () => {\n"
            "  it('adds positives', () => { expect(sum(2,3)).toBe(5); });\n"
            "  it('adds negatives', () => { expect(sum(-2,-3)).toBe(-5); });\n"
            "});\n",
            encoding="utf-8",
        )
    if tid == "task02":
        (d / "src" / "solution.js").write_text(
            "export function reverseWords(s){\n"
            "  return s.trim().split(/\\s+/).reverse().join(' ');\n}\n",
            encoding="utf-8",
        )
        (d / "tests" / "test_solution.test.js").write_text(
            'import { describe, it, expect } from "vitest";\n'
            'import { reverseWords } from "../src/solution.js";\n'
            "describe('reverseWords', () => {\n"
            "  it('reverses words', () => { expect(reverseWords('hello world')).toBe('world hello'); });\n"
            "  it('squashes spaces', () => { expect(reverseWords(' a  b   c ')).toBe('c b a'); });\n"
            "});\n",
            encoding="utf-8",
        )
    if tid == "task03":
        (d / "src" / "solution.js").write_text(
            "export function isPalindrome(s){\n"
            "  const t = (s||'').toLowerCase().replace(/[^a-z0-9]/g,'');\n"
            "  return t === [...t].reverse().join('');\n}\n",
            encoding="utf-8",
        )
        (d / "tests" / "test_solution.test.js").write_text(
            'import { describe, it, expect } from "vitest";\n'
            'import { isPalindrome } from "../src/solution.js";\n'
            "describe('isPalindrome', () => {\n"
            "  it('true cases', () => { expect(isPalindrome('A man, a plan, a canal: Panama')).toBe(true); });\n"
            "  it('false cases', () => { expect(isPalindrome('abc')).toBe(false); });\n"
            "});\n",
            encoding="utf-8",
        )
    if tid == "task04":
        (d / "src" / "solution.js").write_text(
            "export function uniq(arr){\n"
            "  const seen = new Set(); const out = [];\n"
            "  for (const x of arr){ if(!seen.has(x)){ seen.add(x); out.push(x);} }\n"
            "  return out;\n}\n",
            encoding="utf-8",
        )
        (d / "tests" / "test_solution.test.js").write_text(
            'import { describe, it, expect } from "vitest";\n'
            'import { uniq } from "../src/solution.js";\n'
            "describe('uniq', () => {\n"
            "  it('dedupes', () => { expect(uniq([1,1,2,3,2,4])).toEqual([1,2,3,4]); });\n"
            "});\n",
            encoding="utf-8",
        )
    if tid == "task05":
        (d / "src" / "solution.js").write_text(
            "export function freqMap(arr){\n"
            "  const m = new Map();\n"
            "  for(const x of arr){ m.set(x, (m.get(x)||0)+1); }\n"
            "  return m;\n}\n",
            encoding="utf-8",
        )
        (d / "tests" / "test_solution.test.js").write_text(
            'import { describe, it, expect } from "vitest";\n'
            'import { freqMap } from "../src/solution.js";\n'
            "describe('freqMap', () => {\n"
            "  it('counts', () => {\n"
            "    const m = freqMap(['a','b','a']);\n"
            "    expect(m.get('a')).toBe(2); expect(m.get('b')).toBe(1);\n"
            "  });\n"
            "});\n",
            encoding="utf-8",
        )

print(f"Wrote JS tasks to {TASKS}")
