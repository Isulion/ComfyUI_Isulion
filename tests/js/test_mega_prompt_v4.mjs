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

test("help panel opens in the browser language, switches to EN and remembers it", async () => {
  const docBefore = fake.docListeners();
  const node = await createNode(); const j = node._jackpot;
  assert.equal(j.lang, "fr"); assert.equal(j.ui.help.panel.hidden, true);
  click(j.ui.helpBtn); assert.equal(j.ui.help.panel.hidden, false);
  assert.ok(j.ui.help.body.textContent.includes(TEXT.fr.help.sections[0][0]));
  click(j.ui.help.langEn);
  assert.equal(localStorage.getItem("isu-mpv4-lang"), "en"); assert.ok(j.ui.help.body.textContent.includes(TEXT.en.help.sections[0][0]));
  assert.equal(j.ui.reels.theme.name.textContent, TEXT.en.reels.theme);
  document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" })); assert.equal(j.ui.help.panel.hidden, true);
  assert.equal(fake.docListeners(), docBefore + 1);  // only visibilitychange is left
  click(j.ui.helpBtn); click(j.ui.helpBtn); assert.equal(j.ui.help.panel.hidden, true);
  const node2 = await createNode(); assert.equal(node2._jackpot.lang, "en");
  localStorage.removeItem("isu-mpv4-lang");
});

// --- final review fixes -----------------------------------------------------
test("switching an empty reel back on rolls that reel", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload(); const j = node._jackpot;
  j.state.reels.location.enabled = false; j.state.reels.location.text = "";
  click(j.ui.reels.location.btns.toggle); await tick();
  assert.equal(lastRoll().body.state.reels.location.enabled, true); assert.deepEqual(lastRoll().body.reels, ["location"]);
});
test("reels stop spinning when the server returns an error draw", async () => {
  const node = await createNode(); const j = node._jackpot;
  api.responders["/isulion/megaprompt_v4/roll"] = payload({ rolled: [], prompt: "Error: KeyError: x", segments: [{ reel: "error", text: "Error: KeyError: x" }] });
  click(j.ui.lever); await tick(); await tick(); fake.runTimers(5000);
  assert.ok(REELS.every((r) => !j.ui.reels[r].box.classList.contains("isu-mpv4-spin")));
});
test("a lock set while a run was queued survives onExecuted", async () => {
  const node = await createNode(); const j = node._jackpot;
  click(j.ui.reels.subject.btns.lock);                                  // user locks SUBJECT during the run
  const server = { ...readState(null), theme: { name: "anime", locked: false } };
  server.reels.subject.text = "queued subject"; server.reels.location.text = "new place";
  node.onExecuted({ draw: [payload({ state: server, rolled: ["theme", "location"] })] }); fake.runTimers(5000);
  const saved = JSON.parse(node.widgets[0].value);
  assert.equal(saved.reels.subject.locked, true); assert.equal(saved.reels.location.text, "new place"); assert.equal(saved.theme.name, "anime");
});
test("reloading a history line restores its full state", async () => {
  const node = await createNode(); const j = node._jackpot;
  const past = { ...readState(null), theme: { name: "cyberpunk", locked: true }, complexity: "simple" };
  node.onExecuted({ draw: [payload({ state: past, rolled: ["subject"] })] }); fake.runTimers(5000);
  j.state.complexity = "complex"; j.commit();
  click(j.ui.hist.rows[0].row);
  assert.equal(JSON.parse(node.widgets[0].value).complexity, "simple");
});

test("scanline flicker is only on reel icons, text uses a crisp font", async () => {
  await createNode();
  const css = document.getElementById("isu-mpv4-styles").textContent;
  assert.ok(!/isu-mpv4-(crt|screen)::after/.test(css), "no scanline overlay over the text screens");
  assert.ok(/\.isu-mpv4-icon::after\{[^}]*repeating-linear-gradient/.test(css), "icons keep the scanline effect");
  assert.ok(!css.includes("Courier New"), "no blurry Courier New");
});

test("reels spin a symbol strip, slow down, then land one after another", async () => {
  const node = await createNode(); const j = node._jackpot;
  api.responders["/isulion/megaprompt_v4/roll"] = payload({ rolled: ["theme", "subject", "location"] });
  click(j.ui.lever);
  assert.ok(j.ui.reels.subject.box.classList.contains("isu-mpv4-spin")); assert.ok(j.ui.reels.subject.strip.children.length >= 20);
  await tick(); await tick();
  const has = (r, c) => j.ui.reels[r].box.classList.contains(c);
  fake.runTimers(650);                      // first reel braking, last one still at full speed
  assert.ok(has("theme", "isu-mpv4-slow")); assert.ok(!has("location", "isu-mpv4-slow")); assert.ok(has("location", "isu-mpv4-spin"));
  fake.runTimers(700);                      // first reel stopped, last one still moving
  assert.ok(!has("theme", "isu-mpv4-spin")); assert.ok(has("location", "isu-mpv4-spin"));
  fake.runTimers(5000);
  assert.ok(REELS.every((r) => !has(r, "isu-mpv4-spin") && !has(r, "isu-mpv4-slow")));
});

// position of the strip in cells (0 = first cell in the icon window)
const stripCell = (j, name) => -parseFloat(/translate3d\(0,(-?[\d.]+)px,0\)/.exec(j.ui.reels[name].strip.style.transform)[1]) / 34;
function sample(j, name, ms) {
  const cells = [];
  for (let t = 0; t < ms; t += 16) { fake.runTimers(16); fake.flushFrames(); if (j.spins.has(name)) cells.push(stripCell(j, name)); }
  return cells;
}
// unwrap the strip index (it jumps back by one loop to stay on the middle copy)
const unwrap = (k) => k.map((v, i) => v).reduce((acc, v, i) => {
  if (!i) return [v];
  let d = v - (k[i - 1]); while (d > 5) d -= 10; while (d < -5) d += 10;
  acc.push(acc[i - 1] + d); return acc;
}, []);

test("strip motion is continuous: kick, ramp up, steady speed", async () => {
  const node = await createNode(); const j = node._jackpot;
  j.startSpin("style");
  const k = unwrap(sample(j, "style", 1500));
  const steps = k.slice(1).map((v, i) => k[i] - v);          // cells moved per frame (symbols travel down = index decreases)
  assert.ok(steps.slice(0, 4).some((d) => d < 0), "small backward kick first");
  const cruise = steps.slice(-20);
  assert.ok(cruise.every((d) => Math.abs(d - cruise[0]) < 1e-3), "constant speed once launched (0.01 px rounding)");
  assert.ok(cruise[0] > 0.15 && cruise[0] < 0.3, "readable speed (cells per 16 ms)");
  const accel = steps.slice(1).map((d, i) => d - steps[i]);
  assert.ok(accel.every((a) => Math.abs(a) < 0.05), "no velocity jumps");
});

test("a braking reel stops exactly on its result symbol with a small bounce", async () => {
  const node = await createNode(); const j = node._jackpot;
  j.state.reels.style.text = "oil painting";            // final glyph for style is 🎨
  j.startSpin("style"); sample(j, "style", 800);
  j.slowSpin("style");
  const raw = sample(j, "style", 1200);
  const k = unwrap(raw);
  const steps = k.slice(1).map((v, i) => k[i] - v);
  const peak = steps.findIndex((d) => d < 0);
  assert.ok(peak > 5, "brakes forward first");
  assert.ok(steps.slice(0, peak).every((d, i) => i === 0 || d <= steps[i - 1] + 1e-9), "speed only decreases while braking");
  const back = steps.slice(peak).reduce((a, d) => a + Math.min(0, d), 0);
  assert.ok(back < -0.05 && back > -0.3, "small bounce back");
  const final = raw.at(-1);
  assert.ok(Math.abs(final - Math.round(final)) < 1e-6, "ends exactly on a cell");
  assert.equal(j.ui.reels.style.strip.children[Math.round(final)].textContent, "🎨");
  j.landReel("style");
  assert.equal(j.ui.reels.style.glyph.textContent, "🎨"); assert.ok(!j.spins.has("style"));
});

test("the strip spins inside a clipped reel window, never over the name or the buttons", async () => {
  const node = await createNode(); const r = node._jackpot.ui.reels.subject;
  assert.ok(r.face.contains(r.strip), "strip lives in the window");
  assert.ok(!r.face.contains(r.name) && !r.face.contains(r.btns.lock), "name and buttons are outside the window");
  const css = document.getElementById("isu-mpv4-styles").textContent;
  const rule = /\.isu-mpv4-face\{[^}]*\}/.exec(css)?.[0] ?? "";
  assert.ok(/overflow:hidden/.test(rule) && /position:relative/.test(rule), "the window clips the strip");
  assert.ok(/\.isu-mpv4-face::before\{[^}]*linear-gradient/.test(css), "drum shading sits in the window");
});

test("reels still spin when the system asks for reduced motion", async () => {
  const node = await createNode(); const j = node._jackpot;
  globalThis.matchMedia = (q) => ({ matches: q.includes("reduce"), media: q });
  try {
    j.startSpin("effects");
    const k = sample(j, "effects", 600);
    assert.ok(new Set(k.map((v) => v.toFixed(2))).size > 10, "the strip moves");
  } finally { delete globalThis.matchMedia; j.landReel("effects"); }
});

// --- runner (keep last) ---------------------------------------------------
let failures = 0;
for (const [name, fn] of tests) {
  try { await fn(); console.log(`PASS ${name}`); }
  catch (e) { failures++; console.log(`FAIL ${name}\n${e.stack}`); }
}
console.log(`${tests.length - failures}/${tests.length} passed`);
process.exitCode = failures ? 1 : 0;
