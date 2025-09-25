import { describe, it, expect } from "vitest";
import { reverseWords } from "../src/solution.js";
describe('reverseWords', () => {
  it('reverses words', () => { expect(reverseWords('hello world')).toBe('world hello'); });
  it('squashes spaces', () => { expect(reverseWords(' a  b   c ')).toBe('c b a'); });
});
