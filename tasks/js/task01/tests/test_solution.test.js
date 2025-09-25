import { describe, it, expect } from "vitest";
import { sum } from "../src/solution.js";
describe('sum', () => {
  it('adds positives', () => { expect(sum(2,3)).toBe(5); });
  it('adds negatives', () => { expect(sum(-2,-3)).toBe(-5); });
});
