/** @type {import('@stryker-mutator/api/core').PartialStrykerOptions} */
export default {
  // Mutate only your JS task sources
  mutate: ['tasks/js/**/src/**/*.js'],

  // Don't use "files" (deprecated). Ignore everything noisy instead.
  ignorePatterns: [
    'node_modules/**',
    '.venv/**',
    'reports/**',
    '**/*.html',
    '**/*.py',
    '**/.pytest_cache/**'
  ],

  // Use the generic command runner to invoke Vitest (no plugin needed)
  testRunner: 'command',
  commandRunner: { command: 'npx vitest run' },

  // Reporters: strings only; per-reporter options set below
  reporters: ['progress', 'html', 'json'],
  htmlReporter: { baseDir: 'reports/stryker' },
  jsonReporter: { fileName: 'reports/stryker/mutation.json' },

  tempDirName: 'reports/stryker-tmp',
  disableTypeChecks: false,
  thresholds: { high: 80, low: 60, break: 0 },
  coverageAnalysis: 'off'
};