import { describe, it, expect } from "vitest";
import { uniq } from "../src/solution.js";
describe('uniq', () => {
  it('dedupes', () => { expect(uniq([1,1,2,3,2,4])).toEqual([1,2,3,4]); });
});
