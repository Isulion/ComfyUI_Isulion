import { app } from "../../scripts/app.js";

// Logical playfield; the canvas is scaled to fit the node while keeping this aspect ratio.
const W = 240;
const H = 260;
const COLS = 8;
const ROWS = 4;
const ROW_POINTS = [40, 30, 20, 10];
const ROW_COLORS = ["#ff5fa2", "#ffb84d", "#7ee081", "#5fc8ff"];
const KEYS = new Set(["ArrowLeft", "ArrowRight", "KeyA", "KeyD", "Space", "KeyP", "Enter"]);

// 11x8 two-frame invader sprites, one string per row ("x" = pixel)
const SPRITES = [
  ["..x.....x..", "...x...x...", "..xxxxxxx..", ".xx.xxx.xx.", "xxxxxxxxxxx", "x.xxxxxxx.x", "x.x.....x.x", "...xx.xx..."],
  ["..x.....x..", "x..x...x..x", "x.xxxxxxx.x", "xxx.xxx.xxx", "xxxxxxxxxxx", ".xxxxxxxxx.", "..x.....x..", ".x.......x."],
];

function hideWidget(w) {
  if (!w) return;
  w.hidden = true;
  w.type = "converted-widget";
  w.computeSize = () => [0, -4];
  if (w.element) w.element.style.display = "none";
}

function readState(raw) {
  let s;
  try { s = JSON.parse(raw); } catch { s = null; }
  if (!s || typeof s !== "object") s = {};
  const n = (v, d) => (Number.isFinite(v) && v >= 0 ? Math.floor(v) : d);
  return { version: 1, high_score: n(s.high_score, 0), last_score: n(s.last_score, 0), best_wave: Math.max(1, n(s.best_wave, 1)) };
}

class SpaceInvadersGame {
  constructor(node, dataWidget, root) {
    Object.assign(this, { node, dataWidget, root, raf: null, last: 0, visible: true, disposed: false });
    this.canvas = root.appendChild(document.createElement("canvas"));
    this.canvas.tabIndex = 0;  // keyboard input only while the game has focus: no global key capture
    this.canvas.style.cssText = "width:100%;height:100%;display:block;outline:none;touch-action:none;background:#05060f;border-radius:6px";
    this.ctx = this.canvas.getContext("2d");
    this.keys = new Set();

    this.onKeyDown = (e) => this.keyDown(e);
    this.onKeyUp = (e) => this.keyUp(e);
    this.onPointerDown = (e) => { e.stopPropagation(); this.canvas.focus(); if (this.state === "paused") this.setState("playing"); };
    this.onBlur = () => { this.keys.clear(); if (this.state === "playing") this.setState("paused"); };
    this.onContext = (e) => { e.preventDefault(); e.stopPropagation(); };
    this.onWheel = (e) => app.canvas?.canvas?.dispatchEvent(new WheelEvent(e.type, e));  // keep graph zoom working
    this.onVisibility = () => this.schedule();
    this.canvas.addEventListener("keydown", this.onKeyDown);
    this.canvas.addEventListener("keyup", this.onKeyUp);
    this.canvas.addEventListener("pointerdown", this.onPointerDown);
    this.canvas.addEventListener("blur", this.onBlur);
    this.canvas.addEventListener("contextmenu", this.onContext);
    this.canvas.addEventListener("wheel", this.onWheel, { passive: true });
    document.addEventListener("visibilitychange", this.onVisibility);

    this.resizeObserver = new ResizeObserver(() => this.draw());
    this.resizeObserver.observe(root);
    this.intersection = new IntersectionObserver(([e]) => { this.visible = e.isIntersecting; this.schedule(); });
    this.intersection.observe(root);

    this.state = "title";  // before load(): load() draws, and draw() needs a known state
    this.load();
  }

  load() {
    this.saved = readState(this.dataWidget.value);
    if (this.state !== "playing") this.draw();
  }

  commit() {
    const v = JSON.stringify(this.saved);
    if (v === this.dataWidget.value) return;
    this.dataWidget.value = v;
    this.dataWidget.callback?.(v);
    this.node.graph?.change();
    this.node.setDirtyCanvas(true, true);
  }

  // --- game state -------------------------------------------------------
  newGame() {
    this.score = 0;
    this.lives = 3;
    this.wave = 1;
    this.player = { x: W / 2, w: 15, cooldown: 0, hitTimer: 0 };
    this.bullets = [];
    this.bombs = [];
    this.particles = [];
    this.spawnWave();
  }

  spawnWave() {
    this.invaders = [];
    for (let r = 0; r < ROWS; r++)
      for (let c = 0; c < COLS; c++)
        this.invaders.push({ x: 24 + c * 22, y: 34 + r * 16, row: r, alive: true });
    this.dir = 1;
    this.stepTimer = 0;
    this.frame = 0;
    this.bullets = [];
    this.bombs = [];
    this.ufo = null;
    this.ufoTimer = 12 + Math.random() * 10;
  }

  setState(state) {
    this.state = state;
    if (state === "playing") this.last = performance.now();
    this.schedule();
    this.draw();
  }

  gameOver() {
    this.saved.last_score = this.score;
    this.saved.high_score = Math.max(this.saved.high_score, this.score);
    this.saved.best_wave = Math.max(this.saved.best_wave, this.wave);
    this.keys.clear();  // a held Space must not fire on restart
    this.commit();  // one write per game, not per frame
    this.setState("over");
  }

  // --- input ------------------------------------------------------------
  keyDown(e) {
    if (!KEYS.has(e.code)) return;
    e.preventDefault();
    e.stopPropagation();  // keep LiteGraph shortcuts (space-drag, delete…) out of the game
    if (e.code === "Enter" && (this.state === "title" || this.state === "over")) { this.newGame(); this.setState("playing"); return; }
    if (e.code === "KeyP" && (this.state === "playing" || this.state === "paused")) { this.setState(this.state === "playing" ? "paused" : "playing"); return; }
    if (e.code === "Space" && this.state === "title") { this.newGame(); this.setState("playing"); return; }
    this.keys.add(e.code);
  }

  keyUp(e) {
    if (!KEYS.has(e.code)) return;
    e.preventDefault();
    e.stopPropagation();
    this.keys.delete(e.code);
  }

  // --- loop -------------------------------------------------------------
  schedule() {
    const run = !this.disposed && this.state === "playing" && this.visible && !document.hidden;
    if (run) {
      this.raf ??= requestAnimationFrame((t) => this.tick(t));
    } else if (this.raf !== null) {
      cancelAnimationFrame(this.raf);
      this.raf = null;
      if (this.state === "playing" && !this.disposed) this.setState("paused");  // hidden tab or scrolled away
    }
  }

  tick(now) {
    this.raf = null;
    const dt = Math.min(0.05, (now - this.last) / 1000);
    this.last = now;
    this.update(dt);
    this.draw();
    this.schedule();
  }

  update(dt) {
    const p = this.player;
    const left = this.keys.has("ArrowLeft") || this.keys.has("KeyA");
    const right = this.keys.has("ArrowRight") || this.keys.has("KeyD");
    p.x = Math.max(p.w / 2 + 2, Math.min(W - p.w / 2 - 2, p.x + ((right ? 1 : 0) - (left ? 1 : 0)) * 110 * dt));
    p.cooldown -= dt;
    p.hitTimer = Math.max(0, p.hitTimer - dt);
    if (this.keys.has("Space") && p.cooldown <= 0 && this.bullets.length < 2) {
      this.bullets.push({ x: p.x, y: H - 26 });
      p.cooldown = 0.35;
    }

    for (const b of this.bullets) b.y -= 220 * dt;
    for (const b of this.bombs) b.y += (70 + this.wave * 8) * dt;
    this.bullets = this.bullets.filter((b) => b.y > 10);
    this.bombs = this.bombs.filter((b) => b.y < H - 8);

    // invaders march in steps; fewer survivors => faster steps
    const alive = this.invaders.filter((i) => i.alive);
    this.stepTimer -= dt;
    if (this.stepTimer <= 0) {
      this.stepTimer = Math.max(0.05, (0.08 + 0.55 * (alive.length / (ROWS * COLS))) * Math.pow(0.88, this.wave - 1));
      this.frame ^= 1;
      const edge = alive.some((i) => (this.dir > 0 ? i.x + 10 >= W - 4 : i.x - 10 <= 4));
      if (edge) { this.dir *= -1; for (const i of alive) i.y += 8; }
      else for (const i of alive) i.x += 4 * this.dir;
    }

    // random bombs from the lowest invader of a column
    if (alive.length && Math.random() < dt * (0.9 + this.wave * 0.25)) {
      const shooter = alive[Math.floor(Math.random() * alive.length)];
      const lowest = alive.filter((i) => Math.abs(i.x - shooter.x) < 1).reduce((a, b) => (b.y > a.y ? b : a));
      this.bombs.push({ x: lowest.x, y: lowest.y + 6 });
    }

    // mystery ship
    this.ufoTimer -= dt;
    if (!this.ufo && this.ufoTimer <= 0) {
      const fromLeft = Math.random() < 0.5;
      this.ufo = { x: fromLeft ? -12 : W + 12, v: fromLeft ? 50 : -50 };
    }
    if (this.ufo) {
      this.ufo.x += this.ufo.v * dt;
      if (this.ufo.x < -20 || this.ufo.x > W + 20) { this.ufo = null; this.ufoTimer = 15 + Math.random() * 10; }
    }

    // collisions: player bullets
    for (const b of this.bullets) {
      for (const i of alive) {
        if (i.alive && Math.abs(b.x - i.x) < 7 && Math.abs(b.y - i.y) < 5) {
          i.alive = false;
          b.y = -100;
          this.score += ROW_POINTS[i.row];
          this.burst(i.x, i.y, ROW_COLORS[i.row]);
          break;
        }
      }
      if (this.ufo && Math.abs(b.x - this.ufo.x) < 10 && Math.abs(b.y - 20) < 5) {
        this.score += 50 * (1 + Math.floor(Math.random() * 4));
        this.burst(this.ufo.x, 20, "#ff4d4d");
        this.ufo = null;
        this.ufoTimer = 15 + Math.random() * 10;
        b.y = -100;
      }
    }

    // collisions: bombs on the player
    if (p.hitTimer <= 0) {
      for (const b of this.bombs) {
        if (Math.abs(b.x - p.x) < p.w / 2 && b.y > H - 24 && b.y < H - 12) {
          b.y = H + 100;
          this.lives -= 1;
          p.hitTimer = 1.2;
          this.burst(p.x, H - 18, "#ffffff");
          break;
        }
      }
    }

    for (const q of this.particles) { q.x += q.vx * dt; q.y += q.vy * dt; q.life -= dt; }
    this.particles = this.particles.filter((q) => q.life > 0);

    if (this.lives <= 0 || alive.some((i) => i.alive && i.y >= H - 30)) return this.gameOver();
    if (!this.invaders.some((i) => i.alive)) {
      this.wave += 1;
      this.lives = Math.min(5, this.lives + 1);
      this.spawnWave();
    }
  }

  burst(x, y, color) {
    for (let k = 0; k < 10; k++) {
      const a = Math.random() * Math.PI * 2, s = 20 + Math.random() * 50;
      this.particles.push({ x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s, life: 0.4 + Math.random() * 0.3, color });
    }
  }

  // --- rendering --------------------------------------------------------
  draw() {
    if (this.disposed) return;
    const dpr = window.devicePixelRatio || 1;
    const cw = this.canvas.clientWidth, ch = this.canvas.clientHeight;
    if (!cw || !ch) return;
    const bw = Math.round(cw * dpr), bh = Math.round(ch * dpr);
    if (this.canvas.width !== bw || this.canvas.height !== bh) { this.canvas.width = bw; this.canvas.height = bh; }
    const ctx = this.ctx;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.fillStyle = "#05060f";
    ctx.fillRect(0, 0, bw, bh);
    const scale = Math.min(bw / W, bh / H);
    ctx.setTransform(scale, 0, 0, scale, (bw - W * scale) / 2, (bh - H * scale) / 2);
    ctx.imageSmoothingEnabled = false;

    ctx.strokeStyle = "#1c2140";
    ctx.strokeRect(0.5, 0.5, W - 1, H - 1);
    ctx.font = "8px monospace";
    ctx.textBaseline = "top";

    if (this.state === "title" || !this.invaders) return this.drawTitle(ctx);

    // HUD
    ctx.fillStyle = "#c8d0ff";
    ctx.textAlign = "left";
    ctx.fillText(`SCORE ${this.score}`, 6, 5);
    ctx.textAlign = "center";
    ctx.fillText(`WAVE ${this.wave}`, W / 2, 5);
    ctx.textAlign = "right";
    ctx.fillText(`HI ${Math.max(this.saved.high_score, this.score)}`, W - 6, 5);

    for (const i of this.invaders) if (i.alive) this.drawSprite(ctx, SPRITES[this.frame], i.x, i.y, ROW_COLORS[i.row]);
    if (this.ufo) {
      ctx.fillStyle = "#ff4d4d";
      ctx.fillRect(this.ufo.x - 8, 18, 16, 4);
      ctx.fillRect(this.ufo.x - 4, 15, 8, 3);
    }

    const p = this.player;
    if (p.hitTimer <= 0 || Math.floor(p.hitTimer * 10) % 2 === 0) {
      ctx.fillStyle = "#4dff88";
      ctx.fillRect(p.x - p.w / 2, H - 16, p.w, 4);
      ctx.fillRect(p.x - 4, H - 19, 8, 3);
      ctx.fillRect(p.x - 1, H - 22, 2, 3);
    }
    ctx.fillStyle = "#ffffff";
    for (const b of this.bullets) ctx.fillRect(b.x - 0.5, b.y, 1, 5);
    ctx.fillStyle = "#ff8a3d";
    for (const b of this.bombs) ctx.fillRect(b.x - 1, b.y, 2, 4);
    for (const q of this.particles) { ctx.fillStyle = q.color; ctx.globalAlpha = Math.max(0, q.life * 2); ctx.fillRect(q.x, q.y, 1.5, 1.5); }
    ctx.globalAlpha = 1;

    ctx.fillStyle = "#4dff88";
    ctx.fillRect(4, H - 8, W - 8, 1);
    for (let k = 0; k < this.lives; k++) ctx.fillRect(8 + k * 10, H - 6, 7, 3);

    if (this.state === "paused") this.overlay(ctx, "PAUSE", "Cliquez ou P pour reprendre");
    if (this.state === "over") this.overlay(ctx, "GAME OVER", `Score ${this.score}  -  Entrée pour rejouer`);
  }

  drawTitle(ctx) {
    ctx.textAlign = "center";
    ctx.fillStyle = "#4dff88";
    ctx.font = "bold 16px monospace";
    ctx.fillText("SPACE INVADERS", W / 2, 40);
    ctx.font = "8px monospace";
    ROW_COLORS.forEach((c, r) => {
      this.drawSprite(ctx, SPRITES[0], W / 2 - 30, 82 + r * 16, c);
      ctx.fillStyle = "#c8d0ff";
      ctx.textAlign = "left";
      ctx.fillText(`= ${ROW_POINTS[r]} pts`, W / 2 - 14, 79 + r * 16);
    });
    ctx.textAlign = "center";
    ctx.fillStyle = "#c8d0ff";
    ctx.fillText("Cliquez ici puis Entrée pour jouer", W / 2, 160);
    ctx.fillStyle = "#7f88b8";
    ctx.fillText("Flèches / A D : bouger   Espace : tirer", W / 2, 180);
    ctx.fillText("P : pause", W / 2, 192);
    ctx.fillStyle = "#ffb84d";
    ctx.fillText(`HI ${this.saved.high_score}   MEILLEURE VAGUE ${this.saved.best_wave}`, W / 2, 222);
  }

  drawSprite(ctx, rows, cx, cy, color) {
    ctx.fillStyle = color;
    const x0 = Math.round(cx - 5.5), y0 = Math.round(cy - 4);
    rows.forEach((row, y) => { for (let x = 0; x < row.length; x++) if (row[x] === "x") ctx.fillRect(x0 + x, y0 + y, 1, 1); });
  }

  overlay(ctx, title, hint) {
    ctx.fillStyle = "rgba(5,6,15,0.7)";
    ctx.fillRect(0, H / 2 - 24, W, 44);
    ctx.textAlign = "center";
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 14px monospace";
    ctx.fillText(title, W / 2, H / 2 - 18);
    ctx.font = "8px monospace";
    ctx.fillStyle = "#c8d0ff";
    ctx.fillText(hint, W / 2, H / 2 + 4);
  }

  dispose() {
    if (this.disposed) return;
    this.disposed = true;
    if (this.raf !== null) cancelAnimationFrame(this.raf);
    this.raf = null;
    this.resizeObserver.disconnect();
    this.intersection.disconnect();
    document.removeEventListener("visibilitychange", this.onVisibility);
    this.canvas.removeEventListener("keydown", this.onKeyDown);
    this.canvas.removeEventListener("keyup", this.onKeyUp);
    this.canvas.removeEventListener("pointerdown", this.onPointerDown);
    this.canvas.removeEventListener("blur", this.onBlur);
    this.canvas.removeEventListener("contextmenu", this.onContext);
    this.canvas.removeEventListener("wheel", this.onWheel);
    this.root.replaceChildren();
  }
}

app.registerExtension({
  name: "Isulion.SpaceInvaders",
  beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== "IsulionSpaceInvaders") return;

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      const r = onNodeCreated?.apply(this, arguments);
      const data = this.widgets?.find((w) => w.name === "game_state");
      hideWidget(data);
      const root = document.createElement("div");
      root.style.cssText = "width:100%;height:100%";
      const dom = this.addDOMWidget("space_invaders", "isulion-space-invaders", root, {
        getMinHeight: () => 260, hideOnZoom: false, serialize: false,
      });
      this.setSize([Math.max(this.size[0], 320), Math.max(this.size[1], 360)]);
      // root has no size before the first frame; cancel if the node is removed meanwhile
      this._gameRaf = requestAnimationFrame(() => {
        this._gameRaf = null;
        if (!data) return;
        try { this._game = new SpaceInvadersGame(this, data, root); }
        catch (err) { console.error("[Isulion] Space Invaders failed to start", err); }
      });
      dom.onRemove = () => this._disposeGame();
      return r;
    };

    const onConfigure = nodeType.prototype.onConfigure;
    nodeType.prototype.onConfigure = function () {
      const r = onConfigure?.apply(this, arguments);
      this._game?.load();  // widgets_values were just restored
      return r;
    };

    const onRemoved = nodeType.prototype.onRemoved;
    nodeType.prototype.onRemoved = function () {
      const r = onRemoved?.apply(this, arguments);
      this._disposeGame();
      return r;
    };

    // called by both onRemoved and the DOM widget's onRemove; safe to run twice
    nodeType.prototype._disposeGame = function () {
      if (this._gameRaf != null) cancelAnimationFrame(this._gameRaf);
      this._gameRaf = null;
      this._game?.dispose();
      this._game = null;
    };
  },
});
