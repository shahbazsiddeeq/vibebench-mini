#!/usr/bin/env node
import { execFile } from "node:child_process";
import { readFile, readdir, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import fsSync from "node:fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const TASK_ROOT = path.join(ROOT, "tasks", "js");

const exists = await stat(TASK_ROOT).catch(() => null);
if (!exists) {
  console.error(`Missing ${TASK_ROOT}. Run: python scripts/make_js_tasks.py`);
  process.exit(1);
}

// generic async command runner (used for vitest / eslint / npm audit / stryker)
function run(cmd, args, cwd) {
  return new Promise((resolve) => {
    execFile(cmd, args, { cwd, maxBuffer: 10 * 1024 * 1024 }, (err, stdout, stderr) => {
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
  for (const line of stdout.split(/\r?\n/)) {
    const s = line.trim();
    if (!s || s[0] !== "{" || s[s.length - 1] !== "}") continue;
    try {
      const obj = JSON.parse(s);
      const agg = obj?.data?.aggregated ?? obj?.aggregated ?? obj?.testResults ?? null;
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

/* ---------- NEW: Stryker mutation helpers ---------- */

// Try to read Stryker JSON report (support current & older paths)
async function readStrykerScore(taskDir) {
  const candidates = [
    path.join(taskDir, "reports/stryker/mutation.json"),          // our config's jsonReporter
    path.join(taskDir, "reports/mutation/mutation.json"),         // common default
    path.join(taskDir, "reports/mutation/mutation-report.json"),  // older name
  ];
  for (const p of candidates) {
    if (fsSync.existsSync(p)) {
      try {
        const data = JSON.parse(await readFile(p, "utf-8"));
        if (typeof data.mutationScore === "number") return data.mutationScore / 100;
      } catch {}
    }
  }
  return null;
}

async function mutationScore(taskDir) {
  // Prefer project root config if present; fall back to configs/*
  const cfgCandidates = [
    path.join(ROOT, "stryker.conf.mjs"),
    path.join(ROOT, "configs/stryker.vitest.cjs"),
    path.join(ROOT, "configs/stryker.vitest.mjs"),
  ];
  const cfgPath = cfgCandidates.find((p) => fsSync.existsSync(p));

  const args = ["stryker", "run", "--mutate", "src/**/*.js"];
  if (cfgPath) args.push("--configFile", path.relative(taskDir, cfgPath));

  const { code } = await run("npx", args, taskDir);
  if (code !== 0) return null;
  return await readStrykerScore(taskDir);
}

/* ---------- NEW: JS cyclomatic complexity via typhonjs-escomplex ---------- */

async function escomplexScore(taskDir) {
  try {
    const { analyzeModuleSync } = await import("typhonjs-escomplex-module");
    const srcDir = path.join(taskDir, "src");
    const files = [];
    const walk = async (d) => {
      const ents = await readdir(d, { withFileTypes: true });
      for (const ent of ents) {
        const p = path.join(d, ent.name);
        if (ent.isDirectory()) await walk(p);
        else if (p.endsWith(".js")) files.push(p);
      }
    };
    if (fsSync.existsSync(srcDir)) await walk(srcDir);
    if (files.length === 0) return { avg: null, score: null };

    let total = 0;
    let count = 0;
    for (const f of files) {
      const code = await readFile(f, "utf-8");
      const res = analyzeModuleSync(code, { ecmaVersion: 2022 });
      for (const fn of res.functions || []) {
        if (typeof fn.cyclomatic === "number") {
          total += fn.cyclomatic;
          count += 1;
        }
      }
    }
    if (!count) return { avg: null, score: null };
    const avg = total / count;
    const score = avg <= 5 ? 1 : avg >= 15 ? 0 : 1 - (avg - 5) / 10;
    return { avg: +avg.toFixed(3), score: +score.toFixed(3) };
  } catch {
    return { avg: null, score: null };
  }
}

/* ---------- Evaluate one task ---------- */

async function evaluateTask(t) {
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
    depVulns =
      (audit?.metadata?.vulnerabilities &&
        Object.values(audit.metadata.vulnerabilities).reduce((x, y) => x + y, 0)) || 0;
  } catch {
    depVulns = null;
  }
  res.dep_vulns = depVulns;
  res.dep_score = depVulns == null ? null : +(Math.max(0, 1 - Math.min(depVulns, 10) / 10)).toFixed(3);

  // 4) (Optional for now) Security static analysis: leave null to avoid penalizing
  res.security_score = null;

  // --- NEW: JS complexity (escomplex)
  const { avg: ccAvg, score: ccScore } = await escomplexScore(t.path);
  res.complexity_avg = ccAvg;
  res.complexity_score = ccScore;

  // --- NEW: Mutation (Stryker) — skip gracefully if fails / not installed
  res.mutation_score = await mutationScore(t.path);

  // Aggregate across any numeric subscores we have
  const parts = [
    res.correctness,
    res.complexity_score,
    res.lint_score,
    res.dep_score,
    res.mutation_score,
  ].filter((v) => typeof v === "number" && !Number.isNaN(v));
  res.aggregate_score = parts.length
    ? Number((parts.reduce((a, b) => a + b, 0) / parts.length).toFixed(3))
    : 0.0;

  return res;
}

/* ---------- Writers ---------- */

async function writeCSV(results, csvPath) {
  const fields = [
    "id",
    "title",
    "tests_total",
    "tests_passed",
    "tests_failed",
    "tests_errors",
    "correctness",
    "complexity_avg",
    "complexity_score",
    "lint_issues",
    "lint_score",
    "dep_vulns",
    "dep_score",
    "mutation_score",
    "aggregate_score",
  ];
  const lines = [];
  lines.push(fields.join(","));
  for (const t of results.tasks) {
    const row = [
      t.id,
      t.title,
      t.tests?.total ?? "",
      t.tests?.passed ?? "",
      t.tests?.failed ?? "",
      t.tests?.errors ?? "",
      t.correctness ?? "",
      t.complexity_avg ?? "",
      t.complexity_score ?? "",
      t.lint_issues ?? "",
      t.lint_score ?? "",
      t.dep_vulns ?? "",
      t.dep_score ?? "",
      t.mutation_score ?? "",
      t.aggregate_score ?? "",
    ];
    lines.push(row.join(","));
  }
  lines.push(
    [
      "__aggregate__",
      `mean over ${results.aggregate.num_tasks} tasks`,
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      "",
      results.aggregate.mean_score,
    ].join(","),
  );
  await writeFile(csvPath, lines.join("\n") + "\n", "utf-8");
}

async function writeScorecard(results, mdPath) {
  const fmt = (x) => (x == null || Number.isNaN(x) ? "—" : (+x).toFixed(2));
  const lines = [
    "# VibeBench-Mini (JS) Scorecard",
    "",
    `**Overall mean score:** ${results.aggregate.mean_score.toFixed(3)}`,
    "",
    "| Task | Correct | Complx | Lint | Deps | Mut | Aggregate |",
    "|---|---:|---:|---:|---:|---:|---:|",
  ];
  for (const t of results.tasks) {
    lines.push(
      `| ${t.id} | ${fmt(t.correctness)} | ${fmt(t.complexity_score)} | ${fmt(
        t.lint_score,
      )} | ${fmt(t.dep_score)} | ${fmt(t.mutation_score)} | ${fmt(t.aggregate_score)} |`,
    );
  }
  await writeFile(mdPath, lines.join("\n") + "\n", "utf-8");
}

/* ---------- Main ---------- */

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

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
