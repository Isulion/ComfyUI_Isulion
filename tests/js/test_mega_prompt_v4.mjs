// Node harness for web/mega_prompt_v4.js (no npm deps): node tests/js/test_mega_prompt_v4.mjs
import assert from "node:assert/strict";
import { REELS, ROLL_REELS, readState, shortText, pickLang, historyRows, TEXT } from "../../web/mega_prompt_v4_core.js";
import { installFakeDom } from "./fake_dom.mjs";
import { loadExtension } from "./load_extension.mjs";

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

// --- the cabinet ----------------------------------------------------------
const fake = installFakeDom();
const { app, api } = await loadExtension();
const ext = app.extensions.find((e) => e.name === "Isulion.MegaPromptV4");
const nodeType = function () {};
ext?.beforeRegisterNodeDef(nodeType, { name: "IsulionMegaPromptV4" });

function makeNode() {
  const node = {
    widgets: [{ name: "machine_state", value: '{"version": 1}' }],
    size: [300, 200], properties: {},
    graph: { changes: 0, change() { this.changes++; } },
    setSize(s) { this.size = s; }, setDirtyCanvas() {},
    addDOMWidget(name, type, el, opts) { this.dom = { name, type, el, opts }; return this.dom; },
  };
  Object.setPrototypeOf(node, nodeType.prototype);
  return node;
}
const themes = [{ name: "anime", display: "🎌 Anime", icon: "🎌", label: "Anime" }, { name: "cyberpunk", display: "🤖 Cyberpunk", icon: "🤖", label: "Cyberpunk" }];
const payload = (over = {}) => ({ state: { ...readState(null), theme: { name: "anime", locked: false } }, prompt: "hero, forest", rolled: ["theme", "subject", "location"],
  segments: [{ reel: "subject", text: "hero" }, { reel: "location", text: "forest" }], seed: 482913, theme: themes[0], ...over });
const tick = () => new Promise((r) => setImmediate(r));
async function createNode() {
  api.responders["/isulion/megaprompt_v4/themes"] = themes;
  const node = makeNode(); node.onNodeCreated(); fake.flushFrames(); await tick(); await tick();
  return node;
}
const lastRoll = () => api.calls.filter((c) => c.route === "/isulion/megaprompt_v4/roll").at(-1);
const click = (el) => el.dispatchEvent(new Event("click"));

test("registers extension and builds the cabinet once per node", async () => {
  assert.ok(ext); const node = await createNode();
  assert.ok(node._jackpot); assert.equal(node.dom.opts.serialize, false); assert.equal(node.dom.opts.hideOnZoom, false);
  assert.equal(node.widgets[0].hidden, true); assert.equal(node.widgets[0].type, "converted-widget");
  await createNode();
  assert.equal(document.head.children.filter((c) => c.id === "isu-mpv4-styles").length, 1);
});
test("lever posts a roll for all reels and applies the result", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload();
  click(node._jackpot.ui.lever); await tick(); await tick();
  assert.deepEqual(lastRoll().body.reels, REELS); fake.runTimers(5000);
  assert.equal(JSON.parse(node.widgets[0].value).theme.name, "anime");
  assert.ok(node._jackpot.ui.out.textContent.includes("hero, forest")); assert.ok(node.graph.changes >= 1);
  assert.equal(node.properties.isu_mpv4.last.seed, 482913);
});
test("lock writes the state without rolling", async () => {
  const node = await createNode(); const before = api.calls.length;
  click(node._jackpot.ui.reels.subject.btns.lock);
  assert.equal(JSON.parse(node.widgets[0].value).reels.subject.locked, true); assert.equal(api.calls.length, before);
});
test("next theme locks the theme and rerolls the other reels", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload();
  node._jackpot.state.theme.name = "anime";
  click(node._jackpot.ui.reels.theme.btns.next); await tick();
  const { body } = lastRoll(); assert.deepEqual(body.state.theme, { name: "cyberpunk", locked: true }); assert.deepEqual(body.reels, ROLL_REELS);
});
test("onExecuted replays the server result and records history", async () => {
  const node = await createNode(); node.onExecuted({ draw: [payload({ prompt: "from server", segments: [{ reel: "subject", text: "from server" }] })] });
  fake.runTimers(5000);
  assert.equal(node._jackpot.ui.out.textContent.replace(/\s+$/, ""), "from server");
  assert.equal(node.properties.isu_mpv4.draws, 1); assert.ok(node._jackpot.ui.seed.textContent.includes("482913"));
});
test("late roll response is ignored after onExecuted", async () => {
  const node = await createNode(); let resolve; api.responders["/isulion/megaprompt_v4/roll"] = () => new Promise((r) => (resolve = r));
  click(node._jackpot.ui.lever); await tick();
  node.onExecuted({ draw: [payload({ prompt: "server wins", segments: [{ reel: "subject", text: "server wins" }] })] });
  resolve(payload({ prompt: "late", segments: [{ reel: "subject", text: "late" }] })); await tick(); await tick(); fake.runTimers(5000);
  assert.equal(node._jackpot.ui.out.textContent.replace(/\s+$/, ""), "server wins");
});
test("removing the node twice is safe and leaves nothing running", async () => {
  const obsBefore = fake.observers.length, docBefore = fake.docListeners();
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload();
  click(node._jackpot.ui.lever); await tick(); await tick();
  node.onRemoved(); node.dom.onRemove(); node._disposeJackpot();
  assert.equal(node._jackpot, null); assert.equal(fake.pendingTimers(), 0);
  assert.equal(fake.docListeners(), docBefore);
  const mine = fake.observers.slice(obsBefore); assert.ok(mine.length >= 1 && mine.every((o) => o.disconnected));
});

test("inline edit pins a custom subject and rerolls that reel", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload();
  const j = node._jackpot; click(j.ui.reels.subject.btns.edit);
  assert.equal(j.ui.editor.panel.hidden, false); j.ui.editor.input.value = "  my elf queen ";
  j.ui.editor.input.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter" })); await tick();
  assert.equal(lastRoll().body.state.reels.subject.custom, "my elf queen"); assert.deepEqual(lastRoll().body.reels, ["subject"]);
  assert.equal(j.ui.editor.panel.hidden, true);
});
test("escape cancels the inline edit", async () => {
  const node = await createNode(); const before = api.calls.length; const j = node._jackpot;
  click(j.ui.reels.location.btns.edit); j.ui.editor.input.value = "x";
  j.ui.editor.input.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }));
  assert.equal(j.state.reels.location.custom, ""); assert.equal(api.calls.length, before); assert.equal(j.ui.editor.panel.hidden, true);
});
test("clear button removes the custom text and rerolls", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload(); const j = node._jackpot;
  j.state.reels.location.custom = "my castle"; click(j.ui.reels.location.btns.edit);
  assert.equal(j.ui.editor.input.value, "my castle"); click(j.ui.editor.clear); await tick();
  assert.equal(lastRoll().body.state.reels.location.custom, ""); assert.deepEqual(lastRoll().body.reels, ["location"]);
});
test("edit prompt freezes it and the lever unfreezes", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload({ rolled: [], segments: [{ reel: "frozen", text: "fixed text" }], prompt: "fixed text", state: { ...readState(null), frozen_prompt: "fixed text" } });
  const j = node._jackpot; click(j.ui.editBtn); j.ui.editor.textarea.value = "fixed text";
  click(j.ui.editor.ok); await tick();
  assert.equal(lastRoll().body.state.frozen_prompt, "fixed text"); assert.deepEqual(lastRoll().body.reels, []); await tick();
  assert.equal(j.ui.frozenBadge.hidden, false);
  click(j.ui.lever); await tick();
  assert.equal(lastRoll().body.state.frozen_prompt, ""); assert.deepEqual(lastRoll().body.reels, REELS);
});

test("history keeps five lines, favourites first, and reloads a line", async () => {
  const node = await createNode(); const j = node._jackpot;
  for (let n = 1; n <= 7; n++) { node.onExecuted({ draw: [payload({ prompt: `p${n}`, seed: n, segments: [{ reel: "subject", text: `p${n}` }] })] }); fake.runTimers(5000); }
  assert.equal(j.ui.hist.rows.length, 5); assert.equal(j.ui.hist.rows[0].text.textContent, "p7");
  click(j.ui.hist.rows[2].star);                       // p5 becomes a favourite
  node.onExecuted({ draw: [payload({ prompt: "p8", seed: 8 })] }); fake.runTimers(5000);
  assert.equal(j.ui.hist.rows[0].text.textContent, "p5"); assert.equal(j.ui.hist.rows[0].star.textContent, "★");
  assert.equal(j.ui.hist.rows[1].text.textContent, "p8");
  click(j.ui.hist.rows[1].row);
  assert.equal(node.properties.isu_mpv4.last.seed, 8); assert.equal(j.ui.draws.textContent, "TIRAGE #008");
  assert.equal(node.properties.isu_mpv4.history.length, 6);                      // 1 favourite + 5 recent
});
test("history survives a reload through node.properties", async () => {
  const node = await createNode();
  node.onExecuted({ draw: [payload({ prompt: "kept", seed: 3 })] }); fake.runTimers(5000);
  node._jackpot.load();
  assert.equal(node._jackpot.ui.hist.rows[0].text.textContent, "kept");
});

// --- runner (keep last) ---------------------------------------------------
let failures = 0;
for (const [name, fn] of tests) {
  try { await fn(); console.log(`PASS ${name}`); }
  catch (e) { failures++; console.log(`FAIL ${name}\n${e.stack}`); }
}
console.log(`${tests.length - failures}/${tests.length} passed`);
process.exitCode = failures ? 1 : 0;
