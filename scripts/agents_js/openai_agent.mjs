#!/usr/bin/env node
/**
 * JS agent baseline: generate solution.js with OpenAI for each task and evaluate with Vitest + ESLint.
 * Outputs:
 *  - .agent_runs/js/openai-default/tasks/js/<taskXX>/... (generated run tree)
 *  - .agent_runs/js/openai-default/results.csv         (per-task scores)
 *  - .agent_runs/js/openai-default/cost_ledger.jsonl   (one JSON line per call with usage)
 */
import { mkdir, readFile, readdir, stat, writeFile, cp } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";
import OpenAI from "openai";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..", "..");
const TASK_ROOT = path.join(ROOT, "tasks", "js");
const RUN_ROOT  = path.join(ROOT, ".agent_runs", "js", "openai-default");
const MODEL = process.env.OPENAI_MODEL || "gpt-4o-mini";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

function run(cmd, args, cwd) {
  return new Promise((resolve) => {
    execFile(cmd, args, { cwd, maxBuffer: 20 * 1024 * 1024 }, (err, stdout, stderr) =>
      resolve({ code: err ? (err.code ?? 1) : 0, stdout: stdout ?? "", stderr: stderr ?? "" })
    );
  });
}

async function listTasks(root) {
  const items = await readdir(root, { withFileTypes: true });
  return items
    .filter((e) => e.isDirectory() && /^task\d+$/i.test(e.name))
    .map((e) => ({ id: e.name, path: path.join(root, e.name) }))
    .sort((a, b) => a.id.localeCompare(b.id));
}

function extractCode(md) {
  if (!md) return "";
  const fence = /```(?:js|javascript)?\s*([\s\S]*?)```/i;
  const m = md.match(fence);
  if (m && m[1]) return m[1].trim();
  // fallback: return the message as-is
  return md.trim();
}

async function promptForCode(taskDir) {
  const yaml = await readFile(path.join(taskDir, "task.yaml"), "utf8").catch(() => "");
  const testsPath = path.join(taskDir, "tests", "test_solution.test.js");
  const tests = await readFile(testsPath, "utf8").catch(() => "");

  const system = [
    "You are a senior JavaScript engineer.",
    "Write a concise, correct solution that passes the provided Vitest tests.",
    "Export **named** functions required by tests from `src/solution.js`.",
    "Do not include test code. Return ONLY runnable JS code, ideally in a ```js fence."
  ].join(" ");

  const user = [
    "Task metadata (YAML):",
    "-----",
    yaml || "(no task.yaml)",
    "-----",
    "Tests (Vitest):",
    "-----",
    tests || "(no tests found)",
    "-----",
    "Return the full contents of src/solution.js."
  ].join("\n");

  const resp = await openai.chat.completions.create({
    model: MODEL,
    temperature: 0.2,
    messages: [
      { role: "system", content: system },
      { role: "user", content: user }
    ]
  });

  const msg = resp.choices?.[0]?.message?.content ?? "";
  const code = extractCode(msg);
  const usage = resp.usage ?? {};
  return { code, usage };
}

async function evaluate(outDir) {
  // Correctness: Vitest JSON reporter (we parse aggregated counts)
  const v = await run("npx", ["vitest", "run", "--reporter=json", "--silent"], outDir);
  let passed = 0, total = 0;
  for (const line of v.stdout.split(/\r?\n/)) {
    const s = line.trim();
    if (!s || s[0] !== "{" || s[s.length - 1] !== "}") continue;
    try {
      const obj = JSON.parse(s);
      const np = obj?.data?.numPassedTests ?? obj?.numPassedTests;
      const nt = obj?.data?.numTotalTests ?? obj?.numTotalTests;
      if (typeof np === "number" && typeof nt === "number") {
        passed = np; total = nt;
      }
    } catch {}
  }
  const correctness = total ? +(passed / total).toFixed(3) : 0.0;

  // Lint: ESLint JSON
  const l = await run("npx", ["eslint", "src", "--format", "json"], outDir);
  let lintIssues = null;
  try {
    const reports = JSON.parse(l.stdout);
    lintIssues = reports.reduce((a, r) => a + (r.errorCount || 0) + (r.warningCount || 0), 0);
  } catch { lintIssues = null; }
  const lintScore = lintIssues == null ? null : +(Math.max(0, 1 - Math.min(lintIssues, 20) / 20)).toFixed(3);

  // Aggregate: mean of available metrics (correctness + lint)
  const subs = [correctness, lintScore].filter((x) => typeof x === "number");
  const aggregate = subs.length ? +(subs.reduce((a, b) => a + b, 0) / subs.length).toFixed(3) : 0.0;

  return { correctness, lint_issues: lintIssues, lint_score: lintScore, aggregate_score: aggregate };
}

async function ensureRunScaffold(task) {
  const outDir = path.join(RUN_ROOT, "tasks", "js", task.id);
  await mkdir(path.join(outDir, "src"), { recursive: true });
  await mkdir(path.join(outDir, "tests"), { recursive: true });
  await mkdir(path.join(RUN_ROOT), { recursive: true });

  // Copy metadata + tests; do NOT copy original src
  await cp(path.join(task.path, "task.yaml"), path.join(outDir, "task.yaml"), { force: true }).catch(() => {});
  await cp(path.join(task.path, "tests"), path.join(outDir, "tests"), { recursive: true, force: true }).catch(() => {});

  return outDir;
}

async function appendCost(usage, taskId) {
  const line = JSON.stringify({ ts: new Date().toISOString(), model: MODEL, task: taskId, usage }) + "\n";
  await writeFile(path.join(RUN_ROOT, "cost_ledger.jsonl"), line, { flag: "a" });
}

async function writeCSVHeaderOnce(csvPath) {
  try {
    await stat(csvPath);
  } catch {
    await writeFile(csvPath, "id,correctness,lint_issues,lint_score,aggregate_score\n", "utf8");
  }
}

async function main() {
  if (!process.env.OPENAI_API_KEY) {
    console.error("OPENAI_API_KEY missing. Export it first.");
    process.exit(2);
  }
  // ensure node deps at repo root, so vitest/eslint resolve from parent
  const tasks = await listTasks(TASK_ROOT);
  if (!tasks.length) {
    console.error(`No JS tasks in ${TASK_ROOT}. Generate them first (python scripts/make_js_tasks.py).`);
    process.exit(1);
  }

  await mkdir(RUN_ROOT, { recursive: true });
  const csvPath = path.join(RUN_ROOT, "results.csv");
  await writeCSVHeaderOnce(csvPath);

  for (const t of tasks) {
    console.log(`\n==> ${t.id}`);
    const outDir = await ensureRunScaffold(t);

    // 1) ask the model
    const { code, usage } = await promptForCode(t.path);
    if (!code) {
      console.warn(`No code produced for ${t.id}; skipping`);
      continue;
    }
    await writeFile(path.join(outDir, "src", "solution.js"), code, "utf8");
    await appendCost(usage, t.id);

    // 2) evaluate
    const res = await evaluate(outDir);
    const row = `${t.id},${res.correctness},${res.lint_issues ?? ""},${res.lint_score ?? ""},${res.aggregate_score}\n`;
    await writeFile(csvPath, row, { flag: "a" });
    console.log(`results: ${row.trim()}`);
  }

  console.log(`\nWrote: ${csvPath}`);
  console.log(`Cost log: ${path.join(RUN_ROOT, "cost_ledger.jsonl")}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
