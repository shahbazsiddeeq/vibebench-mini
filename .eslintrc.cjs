// Basic, strict but friendly rules for our tiny tasks
const js = require("@eslint/js");

module.exports = {
  root: true,
  languageOptions: { ecmaVersion: 2022, sourceType: "module" },
  ignores: ["**/node_modules/**", "**/dist/**", "**/.agent_runs/**", "**/history/**"],
  plugins: [],
  rules: {
    ...js.configs.recommended.rules,
    "no-unused-vars": ["warn", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
    "no-console": "off"
  }
};