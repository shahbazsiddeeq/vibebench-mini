/// <reference types="vitest" />
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['tasks/js/**/tests/**/*.test.{js,ts}'],
    reporters: ['default', 'json'],
    outputFile: { json: 'reports/vitest.json' }
  },
});
