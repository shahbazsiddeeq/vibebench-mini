/** @type {import('@stryker-mutator/api/core').PartialStrykerOptions} */
export default {
  mutate: ['tasks/js/**/src/**/*.js'],
  testRunner: 'vitest',
  vitest: { configFile: 'vitest.config.mts' },
  reporters: [
    'progress',
    ['html', { baseDir: 'reports/stryker' }],
    ['json', { fileName: 'reports/stryker/mutation.json' }]
  ],
  tempDirName: 'reports/stryker-tmp',
  disableTypeChecks: false,
  thresholds: { high: 80, low: 60, break: 0 },
  coverageAnalysis: 'off',
  ignorePatterns: ['.venv/**','node_modules/**','reports/**','**/*.html']
};
