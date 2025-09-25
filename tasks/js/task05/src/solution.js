export function freqMap(arr){
  const m = new Map();
  for(const x of arr){ m.set(x, (m.get(x)||0)+1); }
  return m;
}
