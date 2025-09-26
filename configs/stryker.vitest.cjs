/** @type {import('@stryker-mutator/api/core').PartialStrykerOptions} */
export default {
  mutate: ['src/**/*.js'],
  testRunner: 'vitest',
  vitest: { configFile: 'vitest.config.mts' },
  reporters: ['progress', 'json', ['html', { baseDir: 'reports/stryker' }]],
  thresholds: { high: 80, low: 60, break: 0 },
  coverageAnalysis: 'off',
};