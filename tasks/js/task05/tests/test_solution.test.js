import { describe, it, expect } from "vitest";
import { freqMap } from "../src/solution.js";
describe('freqMap', () => {
  it('counts', () => {
    const m = freqMap(['a','b','a']);
    expect(m.get('a')).toBe(2); expect(m.get('b')).toBe(1);
  });
});
