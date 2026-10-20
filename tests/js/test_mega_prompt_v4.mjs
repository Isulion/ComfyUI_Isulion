// Node harness for web/mega_prompt_v4.js (no npm deps): node tests/js/test_mega_prompt_v4.mjs
import assert from "node:assert/strict";
import { REELS, ROLL_REELS, readState, shortText, pickLang, historyRows, TEXT } from "../../web/mega_prompt_v4_core.js";

const tests = [];
const test = (name, fn) => tests.push([name, fn]);

// --- core helpers -------------------------------------------------------
test("readState mirrors parse_state defaults", () => {
  const d = readState("garbage");
  assert.equal(d.version, 1); assert.deepEqual(d.theme, { name: "", locked: false });
  assert.deepEqual(d.reels.location, { text: "", locked: false, custom: "", enabled: true });
  assert.deepEqual(readState('{"version": 2}'), d);
  const s = readState({ version: 1, theme: { name: "anime", locked: 1 }, reels: { subject: { text: "x", locked: true } }, complexity: "epic" });
  assert.deepEqual(s.theme, { name: "anime", locked: false }); assert.equal(s.reels.subject.text, "x"); assert.equal(s.complexity, "detailed");
});
test("shortText takes the first significant words", () => {
  assert.equal(shortText("((masterful anime rendition)) of my elf queen, ((as hero))"), "masterful anime");
  assert.equal(shortText("supercalifragilisticexpialidocious"), "supercalifragilistice…");
  assert.equal(shortText(""), "—");
});
test("pickLang", () => {
  assert.equal(pickLang("fr-FR", null), "fr"); assert.equal(pickLang("en-US", null), "en"); assert.equal(pickLang("fr", "en"), "en");
});
test("historyRows puts favourites first and caps at five", () => {
  const h = [1, 2, 3, 4, 5, 6, 7].map((n) => ({ fav: n === 6, payload: { prompt: `p${n}` } }));
  assert.deepEqual(historyRows(h).map((r) => r.payload.prompt), ["p6", "p1", "p2", "p3", "p4"]);
});
test("TEXT has the same keys in both languages", () => {
  const keys = (o, p = "") => Object.keys(o).flatMap((k) => (o[k] && typeof o[k] === "object" && !Array.isArray(o[k]) ? keys(o[k], p + k + ".") : [p + k]));
  assert.deepEqual(keys(TEXT.en), keys(TEXT.fr)); assert.ok(TEXT.fr.help.sections.length >= 8);
  assert.equal(TEXT.fr.help.sections.length, TEXT.en.help.sections.length);
  assert.equal(REELS.length, 5); assert.deepEqual(ROLL_REELS, ["subject", "location", "style", "effects"]);
});

// --- runner (keep last) ---------------------------------------------------
let failures = 0;
for (const [name, fn] of tests) {
  try { await fn(); console.log(`PASS ${name}`); }
  catch (e) { failures++; console.log(`FAIL ${name}\n${e.stack}`); }
}
console.log(`${tests.length - failures}/${tests.length} passed`);
process.exitCode = failures ? 1 : 0;
