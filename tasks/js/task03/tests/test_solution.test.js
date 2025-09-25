import { describe, it, expect } from "vitest";
import { isPalindrome } from "../src/solution.js";
describe('isPalindrome', () => {
  it('true cases', () => { expect(isPalindrome('A man, a plan, a canal: Panama')).toBe(true); });
  it('false cases', () => { expect(isPalindrome('abc')).toBe(false); });
});
