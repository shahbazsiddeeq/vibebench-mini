#!/usr/bin/env node
import { execFile } from "node:child_process";
import { readFile, readdir, stat, writeFile } from "node:fs/promises";
import { createInterface } from "node:readline";
import path from "node:path";
import { fileURLToPath } from "node:url";
import esprima from "esprima";
import estraverse from "estraverse";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const TASK_ROOT = path.join(ROOT, "tasks", "js");

const exists = await stat(TASK_ROOT).catch(() => null);
if (!exists) {
  console.error(`Missing ${TASK_ROOT}. Run: python scripts/make_js_tasks.py`);
  process.exit(1);
}

function run(cmd, args, cwd) {
  return new Promise((resolve) => {
    const p = execFile(cmd, args, { cwd, maxBuffer: 10 * 1024 * 1024 }, (err, stdout, stderr) => {
      resolve({ code: err ? (err.code ?? 1) : 0, stdout: stdout ?? "", stderr: stderr ?? "" });
    });
  });
}

async function discoverTasks(root) {
  const dirs = await readdir(root);
  const out = [];
  for (const d of dirs) {
    const full = path.join(root, d);
    const s = await stat(full).catch(() => null);
    if (s && s.isDirectory() && /^task\d+$/i.test(d)) {
      out.push({ id: d, path: full, title: d });
    }
  }
  out.sort((a, b) => a.id.localeCompare(b.id));
  return out;
}

// Parse Vitest JSON reporter output by scanning lines for aggregated counts
function parseVitestJSONLines(stdout) {
  let passed = 0, total = 0;
  // Vitest JSON reporter prints multiple JSON lines; some include aggregate
  for (const line of stdout.split(/\r?\n/)) {
    const s = line.trim();
    if (!s || s[0] !== "{" || s[s.length - 1] !== "}") continue;
    try {
      const obj = JSON.parse(s);
      const agg = obj?.data?.aggregated ?? obj?.aggregated ?? obj?.testResults ?? null;
      // try common shapes
      const np = obj?.data?.numPassedTests ?? obj?.numPassedTests ?? agg?.numPassedTests;
      const nt = obj?.data?.numTotalTests ?? obj?.numTotalTests ?? agg?.numTotalTests;
      if (typeof np === "number" && typeof nt === "number") {
        passed = np; total = nt;
      }
    } catch {}
  }
  return { passed, total };
}

function mean(xs) {
  const vals = xs.filter((x) => typeof x === "number" && !Number.isNaN(x));
  if (vals.length === 0) return 0;
  return vals.reduce((a, b) => a + b, 0) / vals.length;
}

async function readAllJS(dir) {
  const { readdir, stat, readFile } = await import("node:fs/promises");
  const path = (await import("node:path")).default;
  const out = [];
  async function walk(d) {
    const ents = await readdir(d, { withFileTypes: true });
    for (const e of ents) {
      const full = path.join(d, e.name);
      if (e.isDirectory()) await walk(full);
      else if (e.isFile() && /\.m?js$/i.test(e.name)) out.push(full);
    }
  }
  await walk(dir);
  const files = [];
  for (const f of out) {
    files.push({ path: f, code: await readFile(f, "utf8") });
  }
  return files;
}

/** Compute mean cyclomatic complexity per function across JS files. */
async function jsCyclomaticAvg(srcDir) {
  const files = await readAllJS(srcDir);
  const perFunc = [];

  for (const { code } of files) {
    let ast;
    try {
      ast = esprima.parseModule(code, { loc: false, range: true, tolerant: true });
    } catch {
      continue; // skip parse errors
    }

    const stack = []; // function-level counters
    const bump = () => {
      if (stack.length) stack[stack.length - 1].c++;
    };

    estraverse.traverse(ast, {
      enter(node) {
        // new function scope: start at 1
        if (
          node.type === "FunctionDeclaration" ||
          node.type === "FunctionExpression" ||
          node.type === "ArrowFunctionExpression"
        ) {
          stack.push({ c: 1 });
        }

        // decision points (standard cyclomatic increments)
        switch (node.type) {
          case "IfStatement":
          case "ForStatement":
          case "ForInStatement":
          case "ForOfStatement":
          case "WhileStatement":
          case "DoWhileStatement":
          case "ConditionalExpression":
          case "CatchClause":
            bump(); break;
          case "SwitchCase":
            if (node.test) bump();
            break;
          case "LogicalExpression": // &&, ||
            if (node.operator === "&&" || node.operator === "||") bump();
            break;
          default:
            break;
        }
      },
      leave(node) {
        if (
          node.type === "FunctionDeclaration" ||
          node.type === "FunctionExpression" ||
          node.type === "ArrowFunctionExpression"
        ) {
          const { c } = stack.pop();
          perFunc.push(c);
        }
      },
    });
  }

  if (!perFunc.length) return { avg: null, score: null };
  const avg = perFunc.reduce((a, b) => a + b, 0) / perFunc.length;
  // Normalize like Python: <=5 → 1.0; >=15 → 0.0
  const score = avg <= 5 ? 1 : avg >= 15 ? 0 : 1 - (avg - 5) / 10;
  return { avg: +avg.toFixed(3), score: +score.toFixed(3) };
}


async function evaluateTask(t) {
  const src = path.join(t.path, "src");
  const tests = path.join(t.path, "tests");
  const res = { id: t.id, title: t.title };

  // 1) Correctness (Vitest)
  const v = await run("npx", ["vitest", "run", "--reporter=json", "--silent"], t.path);
  const { passed, total } = parseVitestJSONLines(v.stdout);
  res.tests = { total, passed, failed: Math.max(0, total - passed), errors: v.code !== 0 ? 1 : 0 };
  res.correctness = total ? +(passed / total).toFixed(3) : 0.0;

  // 2) Lint (ESLint)
  const l = await run("npx", ["eslint", "src", "--format", "json"], t.path);
  let lintIssues = null;
  try {
    const reports = JSON.parse(l.stdout);
    lintIssues = reports.reduce((acc, r) => acc + (r.errorCount || 0) + (r.warningCount || 0), 0);
  } catch {
    lintIssues = null;
  }
  res.lint_issues = lintIssues;
  res.lint_score = lintIssues == null ? null : +(Math.max(0, 1 - Math.min(lintIssues, 20) / 20)).toFixed(3);

  // 3) Dependency vulnerabilities (npm audit)
  const a = await run("npm", ["audit", "--json", "--audit-level=low"], t.path);
  let depVulns = null;
  try {
    const audit = JSON.parse(a.stdout);
    depVulns = (audit?.metadata?.vulnerabilities && Object.values(audit.metadata.vulnerabilities).reduce((a, b) => a + b, 0)) || 0;
  } catch { depVulns = null; }
  res.dep_vulns = depVulns;
  res.dep_score = depVulns == null ? null : +(Math.max(0, 1 - Math.min(depVulns, 10) / 10)).toFixed(3);

  // Complexity (cyclomatic) via AST walk
  const cx = await jsCyclomaticAvg(src);
  res.complexity_avg = cx.avg;
  res.complexity_score = cx.score;

  // (Optional) Complexity & Security static analysis for JS can be added later.
//   res.complexity_score = null;
  res.security_score = null;
  res.mutation_score = null;

//   const subs = [res.correctness, res.lint_score, res.dep_score].filter((x) => typeof x === "number");
//   res.aggregate_score = subs.length ? +mean(subs).toFixed(3) : 0.0;
  const subs = [res.correctness, res.lint_score, res.dep_score, res.complexity_score]
    .filter((x) => typeof x === "number");
  res.aggregate_score = subs.length ? +mean(subs).toFixed(3) : 0.0;
  return res;
}

async function writeCSV(results, csvPath) {
  const fields = [
    "id","title","tests_total","tests_passed","tests_failed","tests_errors",
    "correctness","lint_issues","lint_score","dep_vulns","dep_score","aggregate_score"
  ];
  const lines = [];
  lines.push(fields.join(","));
  for (const t of results.tasks) {
    const row = [
      t.id, t.title,
      t.tests?.total ?? "", t.tests?.passed ?? "", t.tests?.failed ?? "", t.tests?.errors ?? "",
      t.correctness ?? "", t.lint_issues ?? "", t.lint_score ?? "", t.dep_vulns ?? "", t.dep_score ?? "",
      t.aggregate_score ?? ""
    ];
    lines.push(row.join(","));
  }
  lines.push(["__aggregate__", `mean over ${results.aggregate.num_tasks} tasks`, "", "", "", "", "", "", "", "", "", results.aggregate.mean_score].join(","));
  await writeFile(csvPath, lines.join("\n") + "\n", "utf-8");
}

async function writeScorecard(results, mdPath) {
  const fmt = (x) => (x == null || Number.isNaN(x) ? "—" : (+x).toFixed(2));
//   const lines = [
//     "# VibeBench-Mini (JS) Scorecard",
//     "",
//     `**Overall mean score:** ${results.aggregate.mean_score.toFixed(3)}`,
//     "",
//     "| Task | Correct | Lint | Deps | Aggregate |",
//     "|---|---:|---:|---:|---:|",
//   ];
//   for (const t of results.tasks) {
//     lines.push(`| ${t.id} | ${fmt(t.correctness)} | ${fmt(t.lint_score)} | ${fmt(t.dep_score)} | ${fmt(t.aggregate_score)} |`);
//   }
  const lines = [
    "# VibeBench-Mini (JS) Scorecard",
    "",
    `**Overall mean score:** ${results.aggregate.mean_score.toFixed(3)}`,
    "",
    "| Task | Correct | Complx | Lint | Deps | Aggregate |",
    "|---|---:|---:|---:|---:|---:|",
  ];
  for (const t of results.tasks) {
    lines.push(`| ${t.id} | ${fmt(t.correctness)} | ${fmt(t.complexity_score)} | ${fmt(t.lint_score)} | ${fmt(t.dep_score)} | ${fmt(t.aggregate_score)} |`);
  }
  await writeFile(mdPath, lines.join("\n") + "\n", "utf-8");
}

async function main() {
  const tasks = await discoverTasks(TASK_ROOT);
  const rows = [];
  for (const t of tasks) {
    rows.push(await evaluateTask(t));
  }
  const meanScore = rows.length ? +mean(rows.map((r) => r.aggregate_score)).toFixed(3) : 0.0;
  const out = { tasks: rows, aggregate: { mean_score: meanScore, num_tasks: rows.length } };
  await writeFile(path.join(ROOT, "results_js.json"), JSON.stringify(out, null, 2), "utf-8");
  await writeCSV(out, path.join(ROOT, "results_js.csv"));
  await writeScorecard(out, path.join(ROOT, "scorecard_js.md"));
  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => { console.error(e); process.exit(1); });