import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";
import { REELS, ROLL_REELS, readState, shortText, pickLang, historyRows, TEXT } from "./mega_prompt_v4_core.js";

// Mega Prompt V4 « Prompt Jackpot »: an arcade slot machine in a DOM widget.
// The Python side owns every draw and the prompt assembly; this file edits the
// hidden machine_state widget, shows what the server returns and animates it.

const NODE_NAME = "IsulionMegaPromptV4";
const ROUTE = "/isulion/megaprompt_v4";
const REEL_ICONS = { subject: "👤", location: "🗺️", style: "🎨", effects: "✨" };
// symbols painted on the spinning strips (the theme strip also uses the theme icons)
const REEL_SYMBOLS = {
  theme: ["🐉", "🚀", "🎌", "🤖", "🌸", "📷", "🏯", "🎃", "🧪", "🌵"],
  subject: ["👤", "🧝", "🤖", "🧙", "🦊", "👩‍🚀", "🐉", "🧜", "🦸", "👸"],
  location: ["🗺️", "🌋", "🌊", "🌌", "🌲", "🏙️", "🏰", "🏜️", "🗻", "🏝️"],
  style: ["🎨", "📷", "🖌️", "🧊", "🎞️", "✏️", "🖼️", "🎭", "💡", "🕹️"],
  effects: ["✨", "⚡", "🔥", "💧", "🌈", "❄️", "💫", "🌙", "☄️", "🌟"],
};
// Reel motion is a pure function of time (no per-frame integration), so dropped
// frames never make it stutter. Units: cells (one symbol) and seconds.
const CELL = 34;          // px per symbol on a strip
const LOOP = 10;          // symbols per loop; the strip holds three copies
const KICK = 0.3;         // backward kick before launch, in cells
const KICK_T = 0.14;      // kick duration
const ACCEL = 40;         // launch acceleration, cells/s²
const VMAX = 13;          // full speed, cells/s (~440 px/s: fast but no strobing)
const BRAKE_T = 0.55;     // braking time onto the result symbol
const OVERSHOOT = 0.15;   // passes the symbol by this much, then settles back
const SETTLE_T = 0.16;
const SPIN_MIN = 600;     // ms a reel spins at least before braking
const STAGGER = 300;      // ms between two reels starting to brake
const LAND_AFTER = (BRAKE_T + SETTLE_T) * 1000;
const LANG_KEY = "isu-mpv4-lang";

let themesPromise = null;  // one /themes request shared by every node

function lsGet(key) {
  try { return localStorage.getItem(key); } catch { return null; }
}
function lsSet(key, value) {
  try { localStorage.setItem(key, value); } catch { /* private mode: language just isn't remembered */ }
}

function hideWidget(w) {
  if (!w) return;
  w.hidden = true;
  w.type = "converted-widget";
  w.computeSize = () => [0, -4];
  if (w.element) w.element.style.display = "none";
}

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
}

const stop = (e) => e.stopPropagation();

const CSS = `
.isu-mpv4-root{position:relative;--isu-mpv4-mono:"Cascadia Mono","Consolas","SF Mono","DejaVu Sans Mono",ui-monospace,monospace;width:100%;height:100%;box-sizing:border-box;font:12px system-ui,sans-serif;color:#e5e7eb;-webkit-font-smoothing:antialiased}
.isu-mpv4-cab{position:relative;height:100%;box-sizing:border-box;display:flex;flex-direction:column;gap:7px;padding:9px;border-radius:14px;
  background:linear-gradient(#24103f,#12081f);border:3px solid #ff2fd0;box-shadow:0 0 18px #ff2fd088,inset 0 0 22px #00e5ff33;overflow:hidden}
/* neon pulse: a cyan copy of the frame fading in and out (opacity only, never repaints the cabinet) */
.isu-mpv4-glow{position:absolute;inset:0;border-radius:14px;border:3px solid #00e5ff;box-shadow:0 0 28px #00e5ffaa,inset 0 0 22px #ff2fd044;
  box-sizing:border-box;pointer-events:none;opacity:0;will-change:opacity;animation:isu-mpv4-neon 3s ease-in-out infinite}
@keyframes isu-mpv4-neon{50%{opacity:1}}
.isu-mpv4-head{display:flex;align-items:center;justify-content:center;position:relative}
.isu-mpv4-marquee{font:bold 15px var(--isu-mpv4-mono);letter-spacing:.2em;color:#ffe600;text-shadow:0 0 8px #ffe600,0 0 18px #ff2fd0}
.isu-mpv4-star{animation:isu-mpv4-blink 1.2s infinite}.isu-mpv4-star+.isu-mpv4-star{animation-delay:.6s}
@keyframes isu-mpv4-blink{50%{opacity:.2}}
.isu-mpv4-helpbtn{position:absolute;right:0;top:-2px;width:22px;height:22px;border-radius:50%;border:2px solid #00e5ff;background:#020617;color:#00e5ff;
  font:bold 12px var(--isu-mpv4-mono);cursor:pointer;box-shadow:0 0 8px #00e5ff;padding:0}
.isu-mpv4-top{display:flex;gap:8px}
.isu-mpv4-crt{flex:1;position:relative;border-radius:12px;background:radial-gradient(ellipse at center,#06122a,#020617 75%);padding:7px;overflow:hidden;
  border:2px solid #0f2a4a;font-family:var(--isu-mpv4-mono)}
/* CRT scanlines only on the reel icons: over text they make it shimmer */
/* scanlines slide by transform on their own layer: animating background-position repainted every icon each frame */
.isu-mpv4-icon::after{content:"";position:absolute;left:0;right:0;top:-3px;bottom:0;background:repeating-linear-gradient(#0000 0 2px,#0006 2px 3px);pointer-events:none;will-change:transform;animation:isu-mpv4-roll .3s linear infinite}
@keyframes isu-mpv4-roll{from{transform:translate3d(0,0,0)}to{transform:translate3d(0,3px,0)}}
.isu-mpv4-reels{display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr 1fr;gap:4px}
.isu-mpv4-reel{position:relative;contain:paint;height:108px;border:2px solid #00e5ff66;border-radius:4px;background:#020617;display:flex;flex-direction:column;
  align-items:center;justify-content:space-between;padding:3px 2px;overflow:hidden}
.isu-mpv4-name,.isu-mpv4-btns{position:relative;z-index:2}
.isu-mpv4-strip{position:absolute;left:0;right:0;top:0;display:none;flex-direction:column;align-items:center;will-change:transform;backface-visibility:hidden;pointer-events:none}
.isu-mpv4-strip span{flex:0 0 34px;height:34px;line-height:34px}
.isu-mpv4-spin .isu-mpv4-strip{display:flex}
.isu-mpv4-spin .isu-mpv4-glyph{visibility:hidden}
.isu-mpv4-label{transition:opacity .25s}
.isu-mpv4-spin .isu-mpv4-label{opacity:0}
.isu-mpv4-name{font-size:9px;letter-spacing:.08em;color:#00e5ff;text-shadow:0 0 4px #00e5ff}
/* the reel window: the strip only ever shows through here, under a drum shading */
.isu-mpv4-face{position:relative;overflow:hidden;flex:1;align-self:stretch;margin:2px 0;border-radius:3px;background:linear-gradient(#0a1428,#030712 50%,#0a1428);
  box-shadow:inset 0 0 0 1px #00e5ff33;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;min-width:0}
.isu-mpv4-face::before{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(#000e,#0000 30%,#0000 70%,#000e)}
.isu-mpv4-icon{position:relative;display:block;width:100%;height:34px;line-height:34px;font-size:24px;text-align:center}
.isu-mpv4-label{font-size:9.5px;color:#cfe9ff;line-height:1.15;max-height:23px;overflow:hidden;word-break:break-word}
.isu-mpv4-btns{display:flex;gap:2px}
.isu-mpv4-btn{background:none;border:0;padding:0 2px;font-size:10px;cursor:pointer;border-radius:3px;color:#cfe9ff}
.isu-mpv4-btn:hover{background:#ffffff22}
.isu-mpv4-locked{border-color:#ffe600;box-shadow:0 0 9px #ffe600}
.isu-mpv4-off{opacity:.3;filter:grayscale(1)}
.isu-mpv4-custom .isu-mpv4-name::after{content:" ✏️"}
.isu-mpv4-reel::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;box-shadow:inset 0 0 18px #ffe600;opacity:0}
.isu-mpv4-land::after{animation:isu-mpv4-flash .45s ease-out}
@keyframes isu-mpv4-flash{from{opacity:1}to{opacity:0}}
.isu-mpv4-stick{width:36px;display:flex;flex-direction:column;align-items:center;padding-top:4px;cursor:pointer;background:none;border:0}
.isu-mpv4-ball{width:30px;height:30px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#ff9af3,#ff2fd0 60%,#7a0a63);box-shadow:0 0 14px #ff2fd0;transition:transform .25s}
.isu-mpv4-shaft{width:6px;height:74px;background:linear-gradient(90deg,#555,#eee,#555);border-radius:3px;transform-origin:bottom;transition:transform .25s}
.isu-mpv4-base{width:26px;height:10px;border-radius:4px;background:#444}
.isu-mpv4-pull .isu-mpv4-shaft{transform:scaleY(.4)}.isu-mpv4-pull .isu-mpv4-ball{transform:translateY(44px)}
.isu-mpv4-pulltxt{font:bold 9px var(--isu-mpv4-mono);color:#ff9af3;margin-top:4px}
.isu-mpv4-panel{display:flex;gap:6px;align-items:center;font-family:var(--isu-mpv4-mono)}
.isu-mpv4-sw{display:flex;border:2px solid #00e5ff66;border-radius:6px;overflow:hidden}
.isu-mpv4-sw button{background:none;border:0;padding:4px 7px;font:9.5px var(--isu-mpv4-mono);color:#7dd3fc;cursor:pointer;letter-spacing:.05em}
.isu-mpv4-sw button.isu-mpv4-on{background:#00e5ff;color:#020617;box-shadow:0 0 10px #00e5ff;font-weight:bold}
.isu-mpv4-lora{flex:1;display:flex;align-items:center;gap:5px;border:2px solid #ff2fd066;border-radius:6px;padding:2px 6px;min-width:0}
.isu-mpv4-lora span{font-size:9px;color:#ff9af3}
.isu-mpv4-lora input{flex:1;min-width:0;background:transparent;border:0;outline:0;color:#ffd6fa;font:11px var(--isu-mpv4-mono)}
.isu-mpv4-screen{position:relative;flex:1;min-height:0;display:flex;flex-direction:column;border-radius:10px;background:#020617;border:2px solid #0f2a4a;padding:8px;font-family:var(--isu-mpv4-mono);overflow:hidden}
.isu-mpv4-hd{display:flex;justify-content:space-between;align-items:center;gap:6px;font-size:9px;color:#ffe600;margin-bottom:4px}
.isu-mpv4-act{background:none;border:0;color:#ffe600;font:9px var(--isu-mpv4-mono);cursor:pointer;padding:0 2px}
.isu-mpv4-act:hover{text-shadow:0 0 6px #ffe600}
.isu-mpv4-frozen{color:#7fe7ff;text-shadow:0 0 5px #7fe7ff}
.isu-mpv4-out{font-size:11.5px;line-height:1.7;min-height:56px;color:#7CFF6B;word-break:break-word}
.isu-mpv4-seg{padding:1px 3px;border-radius:3px;text-shadow:0 0 5px currentColor;animation:isu-mpv4-pop .4s both}
.isu-mpv4-seg-subject,.isu-mpv4-seg-location,.isu-mpv4-seg-style,.isu-mpv4-seg-effects{cursor:pointer}
.isu-mpv4-seg:hover{outline:1px dashed currentColor}
@keyframes isu-mpv4-pop{from{opacity:0}to{opacity:1}}
.isu-mpv4-seg-subject{color:#ff8cc0}.isu-mpv4-seg-location{color:#7fe7ff}.isu-mpv4-seg-style{color:#ffd08a}.isu-mpv4-seg-effects{color:#a6f0a8}
.isu-mpv4-seg-complexity{color:#c4b5fd}.isu-mpv4-seg-lora{color:#e2e8f0;border:1px dashed #64748b}.isu-mpv4-seg-frozen{color:#7fe7ff}.isu-mpv4-seg-error{color:#ff6b6b}
.isu-mpv4-cursor{display:inline-block;width:7px;height:12px;background:#7CFF6B;vertical-align:middle;animation:isu-mpv4-blink .7s infinite}
.isu-mpv4-hint{color:#6b7280}
.isu-mpv4-hist{display:flex;flex-direction:column;gap:3px;margin-top:6px}
.isu-mpv4-histtitle{font-size:9px;color:#ffe600;letter-spacing:.08em}
.isu-mpv4-row{display:flex;gap:6px;align-items:baseline;font-size:10.5px;padding:3px 7px;border-radius:6px;background:#1e1036;color:#d8b4fe;border:1px solid #ff2fd033;cursor:pointer}
.isu-mpv4-row:hover{border-color:#ff2fd0;background:#2a1450}
.isu-mpv4-no{color:#ff2fd0;flex:0 0 auto}
.isu-mpv4-tx{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.isu-mpv4-st{flex:0 0 auto;color:#6b5a8a;background:none;border:0;cursor:pointer;font-size:11px;padding:0}
.isu-mpv4-fav{border-color:#ffe60088;color:#fff3a3}.isu-mpv4-fav .isu-mpv4-st{color:#ffe600;text-shadow:0 0 5px #ffe600}
.isu-mpv4-foot{display:flex;justify-content:space-between;font-size:9px;color:#ffe600;margin-top:auto;padding-top:5px}
.isu-mpv4-overlay{position:absolute;inset:6px;z-index:5;background:#020617f2;border:2px solid #00e5ff;border-radius:8px;padding:6px;display:flex;flex-direction:column;gap:5px}
.isu-mpv4-overlay[hidden]{display:none}
.isu-mpv4-overlay input,.isu-mpv4-overlay textarea{width:100%;box-sizing:border-box;background:#0b1530;border:1px solid #00e5ff66;color:#cfe9ff;font:11px var(--isu-mpv4-mono);padding:4px 6px;border-radius:4px;outline:0}
.isu-mpv4-overlay textarea{flex:1;resize:none;min-height:60px}
.isu-mpv4-list{display:grid;grid-template-columns:1fr 1fr;gap:2px;overflow:auto;min-height:0}
.isu-mpv4-list div{font-size:10px;color:#cfe9ff;padding:3px 5px;border-radius:3px;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.isu-mpv4-list div:hover{background:#00e5ff33}
.isu-mpv4-editrow{display:flex;gap:4px;justify-content:flex-end}
.isu-mpv4-editrow button{background:#0b1530;border:1px solid #00e5ff66;color:#00e5ff;font:10px var(--isu-mpv4-mono);border-radius:4px;cursor:pointer;padding:3px 8px}
.isu-mpv4-help{position:absolute;inset:8px;z-index:10;background:#0b0618;border:2px solid #ff2fd0;border-radius:12px;padding:10px 12px;display:flex;flex-direction:column;gap:6px;box-shadow:0 0 24px #ff2fd088}
.isu-mpv4-help[hidden]{display:none}
.isu-mpv4-helphd{display:flex;align-items:center;gap:6px;font:bold 13px var(--isu-mpv4-mono);color:#ffe600}
.isu-mpv4-helphd span{flex:1}
.isu-mpv4-helphd button{background:none;border:1px solid #ff2fd066;color:#ff9af3;border-radius:4px;cursor:pointer;font:10px var(--isu-mpv4-mono);padding:2px 6px}
.isu-mpv4-helphd button.isu-mpv4-on{background:#ff2fd0;color:#fff}
.isu-mpv4-helpbody{overflow:auto;min-height:0;font:12px/1.45 system-ui,sans-serif;color:#e5e7eb}
.isu-mpv4-helpbody h4{margin:8px 0 2px;color:#00e5ff;font-size:12px}
.isu-mpv4-helpbody p{margin:0}
.isu-mpv4-paused,.isu-mpv4-paused *{animation-play-state:paused!important}
`;

function injectStyles() {
  if (document.getElementById("isu-mpv4-styles")) return;
  const style = el("style", null, CSS);
  style.id = "isu-mpv4-styles";
  document.head.appendChild(style);
}

class PromptJackpot {
  constructor(node, dataWidget, root) {
    Object.assign(this, { node, dataWidget, root, reqId: 0, timers: new Set(), typing: null, disposed: false, visible: true, themes: [] });
    this.lang = pickLang(navigator.language, lsGet(LANG_KEY));
    this.knownThemes = new Map();  // theme entries seen in roll results, before /themes answers
    this.spins = new Map();        // reel name -> { t0, brake } while its strip moves
    this.spinRaf = null;
    this.docCleanups = [];
    injectStyles();
    this.build();

    this.onVisibility = () => this.updatePaused();
    document.addEventListener("visibilitychange", this.onVisibility);
    this.intersection = new IntersectionObserver(([e]) => { this.visible = !!e?.isIntersecting; this.updatePaused(); });
    this.intersection.observe(root);
    this.onWheel = (e) => app.canvas?.canvas?.dispatchEvent(new WheelEvent(e.type, e));  // keep graph zoom working
    root.addEventListener("pointerdown", stop);
    root.addEventListener("wheel", this.onWheel, { passive: true });

    this.load();
    this.loadThemes();
  }

  get t() { return TEXT[this.lang]; }

  // --- DOM ----------------------------------------------------------------
  build() {
    const ui = (this.ui = {});
    this.root.className = "isu-mpv4-root";
    const cab = el("div", "isu-mpv4-cab");
    this.root.appendChild(cab);

    const head = el("div", "isu-mpv4-head");
    ui.marquee = el("span", "isu-mpv4-marquee");
    ui.helpBtn = el("button", "isu-mpv4-helpbtn", "?");
    ui.helpBtn.addEventListener("click", () => this.toggleHelp());
    head.append(el("span", "isu-mpv4-marquee isu-mpv4-star", "★ "), ui.marquee, el("span", "isu-mpv4-marquee isu-mpv4-star", " ★"), ui.helpBtn);

    const top = el("div", "isu-mpv4-top");
    ui.crt = el("div", "isu-mpv4-crt");
    const grid = el("div", "isu-mpv4-reels");
    ui.reels = {};
    for (const name of REELS) grid.appendChild(this.buildReel(name));
    ui.crt.append(grid, this.buildSearch(), this.buildEditor());
    ui.lever = el("button", "isu-mpv4-stick");
    ui.pullText = el("span", "isu-mpv4-pulltxt");
    ui.lever.append(el("span", "isu-mpv4-ball"), el("span", "isu-mpv4-shaft"), el("span", "isu-mpv4-base"), ui.pullText);
    ui.lever.addEventListener("click", () => this.pullLever());
    top.append(ui.crt, ui.lever);

    const panel = el("div", "isu-mpv4-panel");
    const sw = el("div", "isu-mpv4-sw");
    ui.cx = {};
    for (const v of ["simple", "detailed", "complex"]) {
      const b = (ui.cx[v] = el("button"));
      b.addEventListener("click", () => this.setComplexity(v));
      sw.appendChild(b);
    }
    const lora = el("label", "isu-mpv4-lora");
    ui.loraLabel = el("span");
    ui.lora = el("input");
    ui.lora.addEventListener("keydown", (e) => { e.stopPropagation(); if (e.key === "Enter") ui.lora.blur(); });
    ui.lora.addEventListener("change", () => this.setLora(ui.lora.value));
    lora.append(ui.loraLabel, ui.lora);
    panel.append(sw, lora);

    const screen = el("div", "isu-mpv4-screen");
    const hd = el("div", "isu-mpv4-hd");
    ui.promptTitle = el("span");
    ui.frozenBadge = el("span", "isu-mpv4-frozen");
    ui.frozenBadge.hidden = true;
    const acts = el("span");
    ui.copyBtn = el("button", "isu-mpv4-act");
    ui.copyBtn.addEventListener("click", () => this.copyPrompt());
    ui.editBtn = el("button", "isu-mpv4-act");
    ui.editBtn.addEventListener("click", () => this.openPromptEditor());
    acts.append(ui.copyBtn, ui.editBtn);
    hd.append(ui.promptTitle, ui.frozenBadge, acts);
    ui.out = el("div", "isu-mpv4-out");
    ui.hist = el("div", "isu-mpv4-hist");
    ui.hist.rows = [];
    const foot = el("div", "isu-mpv4-foot");
    ui.draws = el("span");
    ui.seed = el("span");
    foot.append(ui.draws, ui.seed);
    screen.append(hd, ui.out, ui.hist, foot);

    cab.append(head, top, panel, screen, this.buildHelp());
    this.root.appendChild(el("div", "isu-mpv4-glow"));
  }

  buildReel(name) {
    const box = el("div", "isu-mpv4-reel");
    const nameEl = el("div", "isu-mpv4-name");
    const face = el("div", "isu-mpv4-face");
    const icon = el("span", "isu-mpv4-icon");
    const glyph = el("span", "isu-mpv4-glyph");
    const strip = el("div", "isu-mpv4-strip");  // spins inside the icon slot, so stopping is seamless
    icon.append(glyph, strip);
    const label = el("span", "isu-mpv4-label");
    face.append(icon, label);
    const btnBox = el("div", "isu-mpv4-btns");
    const btns = {};
    const add = (key, action) => {
      const b = (btns[key] = el("button", "isu-mpv4-btn"));
      b.addEventListener("click", action);
      btnBox.appendChild(b);
    };
    if (name === "theme") add("prev", () => this.stepTheme(-1));
    add("lock", () => this.toggleLock(name));
    if (name === "theme") {
      add("search", () => this.openSearch());
      add("next", () => this.stepTheme(1));
    }
    if (name === "subject" || name === "location") add("edit", () => this.openInlineEdit(name));
    if (name !== "theme" && name !== "subject") add("toggle", () => this.toggleEnabled(name));
    box.append(nameEl, face, btnBox);
    this.ui.reels[name] = { box, name: nameEl, face, icon, glyph, label, btns, strip };
    return box;
  }

  buildSearch() {
    const panel = el("div", "isu-mpv4-overlay");
    panel.hidden = true;
    const input = el("input");
    const list = el("div", "isu-mpv4-list");
    list.addEventListener("wheel", stop, { passive: true });
    input.addEventListener("input", () => this.renderSearch(input.value));
    input.addEventListener("keydown", (e) => {
      e.stopPropagation();
      if (e.key === "Escape") this.closeSearch();
      if (e.key === "Enter") { const first = this.filterThemes(input.value)[0]; if (first) this.setTheme(first.name); }
    });
    panel.append(input, list);
    this.ui.search = { panel, input, list };
    return panel;
  }

  buildEditor() {
    const panel = el("div", "isu-mpv4-overlay");
    panel.hidden = true;
    const input = el("input");
    const textarea = el("textarea");
    textarea.addEventListener("wheel", stop, { passive: true });
    const row = el("div", "isu-mpv4-editrow");
    const clear = el("button", null, "✕");
    const cancel = el("button");
    const ok = el("button");
    row.append(clear, cancel, ok);
    panel.append(input, textarea, row);
    const onKey = (e) => {
      e.stopPropagation();  // Delete/Backspace must not reach LiteGraph while typing
      if (e.key === "Escape") this.closeEditor();
      if (e.key === "Enter" && e.target === input) this.confirmEditor();
    };
    input.addEventListener("keydown", onKey);
    textarea.addEventListener("keydown", onKey);
    ok.addEventListener("click", () => this.confirmEditor());
    cancel.addEventListener("click", () => this.closeEditor());
    clear.addEventListener("click", () => this.clearCustom());
    panel.addEventListener("pointerdown", (e) => { if (e.target === panel) this.closeEditor(); });
    this.ui.editor = { panel, input, textarea, clear, cancel, ok };
    return panel;
  }

  buildHelp() {
    const panel = el("div", "isu-mpv4-help");
    panel.hidden = true;
    const hd = el("div", "isu-mpv4-helphd");
    const title = el("span");
    const langFr = el("button", null, "FR");
    const langEn = el("button", null, "EN");
    const close = el("button");
    langFr.addEventListener("click", () => this.setLang("fr"));
    langEn.addEventListener("click", () => this.setLang("en"));
    close.addEventListener("click", () => this.closeHelp());
    hd.append(title, langFr, langEn, close);
    const body = el("div", "isu-mpv4-helpbody");
    body.addEventListener("wheel", stop, { passive: true });
    panel.append(hd, body);
    this.ui.help = { panel, title, langFr, langEn, close, body };
    return panel;
  }

  // --- state ----------------------------------------------------------------
  load() {
    this.state = readState(this.dataWidget.value);
    this.view = this.node.properties.isu_mpv4 ??= { draws: 0, seed: null, history: [], last: null };
    if (this.view.last?.theme) this.knownThemes.set(this.view.last.theme.name, this.view.last.theme);
    this.render();
  }

  commit() {
    const v = JSON.stringify(this.state);
    if (v === this.dataWidget.value) return;
    this.dataWidget.value = v;
    this.dataWidget.callback?.(v);
    this.node.graph?.change();
    this.node.setDirtyCanvas(true, true);
  }

  saveView() {
    this.node.properties.isu_mpv4 = this.view;
  }

  loadThemes() {
    themesPromise ??= api.fetchApi(`${ROUTE}/themes`)
      .then((r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .catch((err) => { themesPromise = null; throw err; });
    themesPromise
      .then((list) => { if (this.disposed || !Array.isArray(list)) return; this.themes = list; this.renderReel("theme"); })
      .catch((err) => console.warn("[Isulion] Mega Prompt V4: theme list unavailable", err));
  }

  themeInfo() {
    const name = this.state.theme.name;
    return this.themes.find((t) => t.name === name) ?? this.knownThemes.get(name) ?? { name, icon: "🎰", label: name || "?" };
  }

  // --- server ---------------------------------------------------------------
  async roll(reels) {
    const id = ++this.reqId;
    let r, payload;
    try {
      r = await api.fetchApi(`${ROUTE}/roll`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: this.state, reels }),
      });
      payload = await r.json();
    } catch (err) {
      if (id === this.reqId && !this.disposed) this.showError(String(err?.message ?? err));
      return;
    }
    if (id !== this.reqId || this.disposed) return;  // a newer roll or an execution result won
    if (!r.ok) return this.showError(payload?.error ?? `HTTP ${r.status}`);
    const changed = payload.rolled?.length > 0;
    this.applyResult(payload, { animate: changed, record: changed, merge: true });
  }

  applyResult(payload, { animate, record, merge = false }) {
    if (merge) this.mergeRolled(payload);
    else this.state = readState(payload.state);
    this.commit();
    if (payload.theme?.name) this.knownThemes.set(payload.theme.name, payload.theme);
    this.view.last = payload;
    this.view.seed = payload.seed ?? null;
    if (record) {
      this.view.draws += 1;
      this.pushHistory(payload);
    }
    this.saveView();
    this.renderFooter();
    const segments = payload.segments ?? [];
    if (animate) {
      this.spinReels(payload.rolled ?? [], () => { this.renderReels(); this.typePrompt(segments); });
    } else {
      this.stopSpins();
      this.renderReels();
      this.renderPrompt(segments);
    }
  }

  onExecuted(payload) {
    if (!payload) return;
    this.reqId++;  // any roll still in flight is now stale
    if (payload.rolled?.length) this.pullAnimation();  // the run pulls the lever too
    this.applyResult(payload, { animate: true, record: true, merge: true });
  }

  // The server rolled a snapshot taken when the request was sent: take only the
  // drawn texts, so locks/toggles/settings changed in the meantime are kept.
  mergeRolled(payload) {
    const server = readState(payload.state);
    for (const name of payload.rolled ?? []) {
      if (name === "theme") this.state.theme.name = server.theme.name;
      else if (this.state.reels[name]) this.state.reels[name].text = server.reels[name].text;
    }
    if (!this.state.theme.name) this.state.theme.name = server.theme.name;
  }

  showError(message) {
    this.stopSpins();
    this.renderPrompt([{ reel: "error", text: `${this.t.error}: ${message}` }]);
  }

  // --- actions --------------------------------------------------------------
  pullLever() {
    if (this.state.frozen_prompt) this.state.frozen_prompt = "";
    this.pullAnimation();
    for (const name of this.freeReels()) this.startSpin(name);
    this.roll(REELS);
  }

  freeReels() {
    return REELS.filter((name) => (name === "theme"
      ? !this.state.theme.locked
      : !this.state.reels[name].locked && this.state.reels[name].enabled !== false));
  }

  toggleLock(name) {
    const target = name === "theme" ? this.state.theme : this.state.reels[name];
    target.locked = !target.locked;
    this.commit();
    this.renderReel(name);
  }

  toggleEnabled(name) {
    const reel = this.state.reels[name];
    reel.enabled = !reel.enabled;
    this.commit();
    this.renderReel(name);
    // a reel that was off during earlier draws has no text yet: draw it now
    this.roll(reel.enabled && !reel.text && !reel.locked ? [name] : []);
  }

  stepTheme(dir) {
    const list = this.themes;
    if (!list.length) return;
    const i = list.findIndex((t) => t.name === this.state.theme.name);
    const j = i < 0 ? 0 : (i + dir + list.length) % list.length;
    this.setTheme(list[j].name);
  }

  setTheme(name) {
    this.state.theme = { name, locked: true };
    this.commit();
    this.closeSearch();
    this.renderReel("theme");
    for (const r of ROLL_REELS) if (this.freeReels().includes(r)) this.startSpin(r);
    this.roll(ROLL_REELS);
  }

  setComplexity(v) {
    this.state.complexity = v;
    this.commit();
    this.renderComplexity();
    this.roll([]);
  }

  setLora(v) {
    this.state.lora = v;
    this.commit();
    this.roll([]);
  }

  copyPrompt() {
    navigator.clipboard?.writeText(this.view.last?.prompt ?? "")?.catch?.(() => {});
    this.ui.copyBtn.textContent = this.t.copied;
    this.setTimer(() => { this.ui.copyBtn.textContent = this.t.copy; }, 1200);
  }

  // search panel
  filterThemes(q) {
    const needle = String(q).trim().toLowerCase();
    return this.themes.filter((t) => t.label.toLowerCase().includes(needle));
  }

  openSearch() {
    const { panel, input } = this.ui.search;
    panel.hidden = false;
    input.value = "";
    this.renderSearch("");
    input.focus();
  }

  closeSearch() {
    this.ui.search.panel.hidden = true;
  }

  renderSearch(q) {
    const rows = this.filterThemes(q).map((t) => {
      const row = el("div", null, `${t.icon} ${t.label}`);
      row.addEventListener("click", () => this.setTheme(t.name));
      return row;
    });
    this.ui.search.list.replaceChildren(...rows);
  }

  // on-screen editors: custom subject/location text, or the whole frozen prompt
  openInlineEdit(reel) {
    const { panel, input, textarea, clear } = this.ui.editor;
    this.editing = { reel };
    input.hidden = false;
    clear.hidden = false;
    textarea.hidden = true;
    input.value = this.state.reels[reel].custom;
    panel.hidden = false;
    input.focus();
  }

  openPromptEditor() {
    const { panel, input, textarea, clear } = this.ui.editor;
    this.editing = { prompt: true };
    input.hidden = true;
    clear.hidden = true;
    textarea.hidden = false;
    textarea.value = this.state.frozen_prompt || (this.view.last?.prompt ?? "");
    panel.hidden = false;
    textarea.focus();
  }

  closeEditor() {
    this.editing = null;
    this.ui.editor.panel.hidden = true;
  }

  confirmEditor() {
    const editing = this.editing;
    if (!editing) return;
    this.closeEditor();
    if (editing.prompt) {
      this.state.frozen_prompt = this.ui.editor.textarea.value;
      this.commit();
      this.roll([]);
    } else {
      this.setCustom(editing.reel, this.ui.editor.input.value.trim());
    }
  }

  clearCustom() {
    const editing = this.editing;
    if (!editing?.reel) return;
    this.closeEditor();
    this.setCustom(editing.reel, "");
  }

  setCustom(reel, text) {
    this.state.reels[reel].custom = text;
    this.commit();
    this.renderReel(reel);
    this.roll([reel]);
  }

  // last draws: up to 5 favourites plus the 5 most recent others
  pushHistory(payload) {
    const history = [{ payload, fav: false }, ...this.view.history];
    const favs = history.filter((h) => h.fav).slice(0, 5);
    const rest = history.filter((h) => !h.fav).slice(0, 5);
    this.view.history = history.filter((h) => favs.includes(h) || rest.includes(h));
    this.renderHistory();
  }

  renderHistory() {
    const hist = this.ui.hist;
    hist.rows = historyRows(this.view.history).map((item, i) => {
      const row = el("div", "isu-mpv4-row" + (item.fav ? " isu-mpv4-fav" : ""));
      const text = el("span", "isu-mpv4-tx", item.payload?.prompt ?? "");
      const star = el("button", "isu-mpv4-st", item.fav ? "★" : "☆");
      row.append(el("span", "isu-mpv4-no", String(i + 1).padStart(2, "0")), text, star);
      star.addEventListener("click", (e) => {
        e.stopPropagation();  // starring must not also reload the line
        item.fav = !item.fav;
        this.saveView();
        this.renderHistory();
      });
      row.addEventListener("click", () => this.applyResult(item.payload, { animate: false, record: false }));
      return { row, text, star };
    });
    const title = el("div", "isu-mpv4-histtitle", this.t.history);
    hist.replaceChildren(title, ...hist.rows.map((r) => r.row));
  }

  // help panel, EN / FR
  toggleHelp() {
    this.ui.help.panel.hidden ? this.openHelp() : this.closeHelp();
  }

  openHelp() {
    this.renderHelp();
    this.ui.help.panel.hidden = false;
    if (this.removeHelpKey) return;
    const onKey = (e) => { if (e.key === "Escape") { e.stopPropagation(); this.closeHelp(); } };
    document.addEventListener("keydown", onKey, true);
    this.removeHelpKey = () => {
      document.removeEventListener("keydown", onKey, true);
      this.docCleanups = this.docCleanups.filter((fn) => fn !== this.removeHelpKey);
      this.removeHelpKey = null;
    };
    this.docCleanups.push(this.removeHelpKey);
  }

  closeHelp() {
    this.ui.help.panel.hidden = true;
    this.removeHelpKey?.();
  }

  setLang(lang) {
    this.lang = lang;
    lsSet(LANG_KEY, lang);
    this.renderLabels();
    this.renderFooter();
    this.renderHistory();
    if (!this.view.last) this.renderPrompt([]);
    this.renderHelp();
  }

  renderHelp() {
    const { title, body, close, langFr, langEn } = this.ui.help;
    const help = this.t.help;
    title.textContent = help.title;
    close.textContent = help.close;
    langFr.classList.toggle("isu-mpv4-on", this.lang === "fr");
    langEn.classList.toggle("isu-mpv4-on", this.lang === "en");
    body.replaceChildren(...help.sections.flatMap(([h, p]) => [el("h4", null, h), el("p", null, p)]));
  }

  // --- rendering ------------------------------------------------------------
  render() {
    this.renderLabels();
    this.renderReels();
    this.renderComplexity();
    this.ui.lora.value = this.state.lora;
    this.renderFooter();
    this.renderHistory();
    if (this.view.last) this.renderPrompt(this.view.last.segments ?? []);
    else this.renderPrompt([]);
  }

  renderLabels() {
    const t = this.t, ui = this.ui;
    ui.marquee.textContent = t.marquee;
    for (const name of REELS) ui.reels[name].name.textContent = t.reels[name];
    ui.pullText.textContent = t.pull;
    for (const [v, b] of Object.entries(ui.cx)) b.textContent = t.complexity[v];
    ui.loraLabel.textContent = t.lora;
    ui.promptTitle.textContent = t.promptTitle;
    ui.copyBtn.textContent = t.copy;
    ui.editBtn.textContent = t.edit;
    ui.frozenBadge.textContent = t.frozenBadge;
    ui.search.input.placeholder = t.searchPlaceholder;
    ui.editor.input.placeholder = t.editPlaceholder;
    ui.editor.cancel.textContent = t.cancel;
    ui.editor.ok.textContent = t.ok;
  }

  renderReels() {
    for (const name of REELS) this.renderReel(name);
  }

  reelView(name) {
    let icon, label, locked, off = false, custom = false;
    if (name === "theme") {
      const info = this.themeInfo();
      icon = info.icon;
      label = info.label;
      locked = this.state.theme.locked;
    } else {
      const reel = this.state.reels[name];
      custom = !!reel.custom;
      icon = custom ? "✏️" : REEL_ICONS[name];
      label = shortText(reel.text || reel.custom);
      locked = reel.locked;
      off = reel.enabled === false;
    }
    return { icon, label, locked, off, custom };
  }

  renderReel(name) {
    const r = this.ui.reels[name];
    const { icon, label, locked, off, custom } = this.reelView(name);
    if (r.btns.toggle) r.btns.toggle.textContent = off ? "🚫" : "👁";
    r.glyph.textContent = icon;
    r.label.textContent = label;
    r.btns.lock.textContent = locked ? "🔒" : "🔓";
    if (r.btns.prev) { r.btns.prev.textContent = "◀"; r.btns.next.textContent = "▶"; r.btns.search.textContent = "🔍"; }
    if (r.btns.edit) r.btns.edit.textContent = "✏️";
    r.box.classList.toggle("isu-mpv4-locked", locked);
    r.box.classList.toggle("isu-mpv4-off", off);
    r.box.classList.toggle("isu-mpv4-custom", custom);
  }

  renderComplexity() {
    for (const [v, b] of Object.entries(this.ui.cx)) b.classList.toggle("isu-mpv4-on", v === this.state.complexity);
  }

  renderFooter() {
    this.ui.draws.textContent = this.t.draw + String(this.view.draws).padStart(3, "0");
    this.ui.seed.textContent = this.t.seed + (this.view.seed ?? "—");
  }

  cursor() {
    return el("span", "isu-mpv4-cursor");
  }

  renderPrompt(segments) {
    clearInterval(this.typing);
    this.typing = null;
    const out = this.ui.out;
    out.replaceChildren();
    if (!segments.length) out.appendChild(el("span", "isu-mpv4-hint", this.t.emptyHint));
    segments.forEach((seg, i) => {
      if (i) out.append(", ");
      const span = el("span", `isu-mpv4-seg isu-mpv4-seg-${seg.reel}`, seg.text);
      if (ROLL_REELS.includes(seg.reel)) span.addEventListener("click", () => this.roll([seg.reel]));
      out.appendChild(span);
    });
    out.appendChild(this.cursor());
    this.ui.frozenBadge.hidden = !this.state.frozen_prompt.trim();
  }

  typePrompt(segments) {
    clearInterval(this.typing);
    const full = segments.map((s) => s.text).join(", ");
    if (!full) return this.renderPrompt(segments);
    let k = 0;
    this.typing = setInterval(() => {
      k += 3;
      this.ui.out.textContent = full.slice(0, k);
      this.ui.out.appendChild(this.cursor());
      if (k >= full.length) this.renderPrompt(segments);
    }, 14);
  }

  // --- animation ------------------------------------------------------------
  setTimer(fn, ms) {
    const id = setTimeout(() => { this.timers.delete(id); if (!this.disposed) fn(); }, ms);
    this.timers.add(id);
  }

  pullAnimation() {
    this.ui.lever.classList.add("isu-mpv4-pull");
    this.setTimer(() => this.ui.lever.classList.remove("isu-mpv4-pull"), 320);
  }

  // Reels: kick back, launch, run at full speed, brake onto the result, left to right.
  spinReels(names, done) {
    for (const name of REELS) if (!names.includes(name) && this.spins.has(name)) this.landReel(name);
    if (!names.length) return done();
    const now = performance.now();
    names.forEach((name, i) => {
      if (!this.spins.has(name)) this.startSpin(name);
      const spun = now - this.spins.get(name).t0;
      const brakeAt = Math.max(0, SPIN_MIN - spun) + STAGGER * i;
      this.setTimer(() => this.slowSpin(name), brakeAt);
      this.setTimer(() => {
        this.landReel(name);
        if (i === names.length - 1) done();
      }, brakeAt + LAND_AFTER);
    });
  }

  startSpin(name) {
    const r = this.ui.reels[name];
    if (!this.spins.has(name)) {
      const pool = name === "theme" && this.themes.length ? this.themes.map((t) => t.icon) : REEL_SYMBOLS[name];
      const loop = Array.from({ length: LOOP }, () => pool[Math.floor(Math.random() * pool.length)]);
      loop[0] = r.glyph.textContent || loop[0];  // the strip starts on the symbol already shown
      r.strip.replaceChildren(...[...loop, ...loop, ...loop].map((c) => el("span", null, c)));
      this.spins.set(name, { t0: performance.now(), brake: null });
    }
    r.box.classList.remove("isu-mpv4-land", "isu-mpv4-slow");
    r.box.classList.add("isu-mpv4-spin");
    this.paintStrip(name, performance.now());
    this.spinRaf ??= requestAnimationFrame((t) => this.spinFrame(t));
  }

  // Plan a braking curve that keeps the current speed and stops exactly on the
  // result symbol, which is written into the strip at the landing cell.
  slowSpin(name) {
    const spin = this.spins.get(name);
    if (!spin || spin.brake) return;
    const now = performance.now();
    const u0 = this.travel(spin, now);
    const v0 = this.freeSpeed((now - spin.t0) / 1000);
    const wanted = Math.max(v0 * BRAKE_T / 2, 3);  // ~linear speed decay; never lands on a visible cell
    const end = -Math.round(-(u0 + wanted));      // landing travel: a whole number of cells
    spin.brake = { t0: now, u0, v0, d: end - u0 };
    const cells = this.ui.reels[name].strip.children;
    const idx = ((-end % LOOP) + LOOP) % LOOP;
    for (const k of [idx, idx + LOOP, idx + 2 * LOOP]) cells[k].textContent = this.reelView(name).icon;
    this.ui.reels[name].box.classList.add("isu-mpv4-slow");
  }

  landReel(name) {
    this.spins.delete(name);
    const box = this.ui.reels[name].box;
    box.classList.remove("isu-mpv4-spin", "isu-mpv4-slow");
    void box.offsetWidth;  // restart the flash
    box.classList.add("isu-mpv4-land");
    this.renderReel(name);
  }

  stopSpins() {
    for (const name of [...this.spins.keys()]) {
      this.spins.delete(name);
      this.ui.reels[name].box.classList.remove("isu-mpv4-spin", "isu-mpv4-slow");
    }
  }

  // speed (cells/s) of a free-running reel t seconds after launch
  freeSpeed(t) {
    if (t < KICK_T) return -KICK * Math.PI / KICK_T * Math.cos(Math.PI * t / KICK_T);
    const v1 = KICK * Math.PI / KICK_T, ta = (VMAX - v1) / ACCEL, tt = t - KICK_T;
    return tt < ta ? v1 + ACCEL * tt : VMAX;
  }

  // distance travelled (cells) at time `now`; symbols move down as it grows
  travel(spin, now) {
    const b = spin.brake;
    if (b) {
      const t = (now - b.t0) / 1000;
      if (t >= BRAKE_T + SETTLE_T) return b.u0 + b.d;
      if (t >= BRAKE_T) {  // settle back from the overshoot (smoothstep: no speed jump)
        const s = (t - BRAKE_T) / SETTLE_T;
        return b.u0 + b.d + OVERSHOOT * (1 - s * s * (3 - 2 * s));
      }
      // cubic Hermite: starts at the current speed, ends still, OVERSHOOT past the symbol
      const s = t / BRAKE_T;
      return b.u0 + b.v0 * BRAKE_T * (s * s * s - 2 * s * s + s) + (b.d + OVERSHOOT) * (3 * s * s - 2 * s * s * s);
    }
    const t = (now - spin.t0) / 1000;
    if (t < KICK_T) return -KICK * Math.sin(Math.PI * t / KICK_T);
    const v1 = KICK * Math.PI / KICK_T, ta = (VMAX - v1) / ACCEL, tt = t - KICK_T;
    if (tt < ta) return v1 * tt + ACCEL * tt * tt / 2;
    return v1 * ta + ACCEL * ta * ta / 2 + VMAX * (tt - ta);
  }

  // one rAF loop paints every moving strip
  spinFrame(now) {
    this.spinRaf = null;
    if (this.disposed || !this.spins.size) return;
    for (const name of this.spins.keys()) this.paintStrip(name, now);
    this.spinRaf = requestAnimationFrame((t) => this.spinFrame(t));
  }

  paintStrip(name, now) {
    const spin = this.spins.get(name);
    if (!spin) return;
    // no prefers-reduced-motion freeze: the spin is short, user-triggered and is the whole point
    // of the machine (a frozen strip just showed overlapping symbols on systems with animations off)
    const u = this.travel(spin, now);
    const k = LOOP + (((-u % LOOP) + LOOP) % LOOP);  // stay on the middle copy of the loop
    this.ui.reels[name].strip.style.transform = `translate3d(0,${(-k * CELL).toFixed(2)}px,0)`;
  }

  updatePaused() {
    this.root.classList.toggle("isu-mpv4-paused", !this.visible || document.hidden);
  }

  dispose() {
    if (this.disposed) return;
    this.disposed = true;
    this.reqId++;
    for (const id of this.timers) clearTimeout(id);
    this.timers.clear();
    clearInterval(this.typing);
    this.typing = null;
    if (this.spinRaf !== null) cancelAnimationFrame(this.spinRaf);
    this.spinRaf = null;
    this.spins.clear();
    this.intersection.disconnect();
    document.removeEventListener("visibilitychange", this.onVisibility);
    for (const fn of this.docCleanups.splice(0)) fn();
    this.root.removeEventListener("pointerdown", stop);
    this.root.removeEventListener("wheel", this.onWheel);
    this.root.replaceChildren();
  }
}

app.registerExtension({
  name: "Isulion.MegaPromptV4",
  beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== NODE_NAME) return;

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      const r = onNodeCreated?.apply(this, arguments);
      const data = this.widgets?.find((w) => w.name === "machine_state");
      hideWidget(data);
      const root = document.createElement("div");
      const dom = this.addDOMWidget("prompt_jackpot", "isulion-prompt-jackpot", root, {
        getMinHeight: () => 560, hideOnZoom: false, serialize: false,
      });
      this.setSize([Math.max(this.size[0], 480), Math.max(this.size[1], 640)]);
      // root has no size before the first frame; cancel if the node is removed meanwhile
      this._jackpotRaf = requestAnimationFrame(() => {
        this._jackpotRaf = null;
        if (!data) return;
        try { this._jackpot = new PromptJackpot(this, data, root); }
        catch (err) { console.error("[Isulion] Mega Prompt V4 failed to start", err); }
      });
      dom.onRemove = () => this._disposeJackpot();
      return r;
    };

    const onConfigure = nodeType.prototype.onConfigure;
    nodeType.prototype.onConfigure = function () {
      const r = onConfigure?.apply(this, arguments);
      this._jackpot?.load();  // widgets_values and properties were just restored
      return r;
    };

    const onExecuted = nodeType.prototype.onExecuted;
    nodeType.prototype.onExecuted = function (message) {
      const r = onExecuted?.apply(this, arguments);
      this._jackpot?.onExecuted(message?.draw?.[0]);  // message is the "ui" dict, values are lists
      return r;
    };

    const onRemoved = nodeType.prototype.onRemoved;
    nodeType.prototype.onRemoved = function () {
      const r = onRemoved?.apply(this, arguments);
      this._disposeJackpot();
      return r;
    };

    // called by both onRemoved and the DOM widget's onRemove; safe to run twice
    nodeType.prototype._disposeJackpot = function () {
      if (this._jackpotRaf != null) cancelAnimationFrame(this._jackpotRaf);
      this._jackpotRaf = null;
      this._jackpot?.dispose();
      this._jackpot = null;
    };
  },
});
