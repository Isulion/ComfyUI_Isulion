// Minimal fake browser for the extension tests: just what web/mega_prompt_v4.js touches.

class FakeEvent {
  constructor(type, init = {}) {
    Object.assign(this, init);
    this.type = type;
    this.defaultPrevented = false;
    this.propagationStopped = false;
  }
  preventDefault() { this.defaultPrevented = true; }
  stopPropagation() { this.propagationStopped = true; }
}

class Target {
  constructor() { this._listeners = new Map(); }
  addEventListener(type, fn) {
    if (!this._listeners.has(type)) this._listeners.set(type, new Set());
    this._listeners.get(type).add(fn);
  }
  removeEventListener(type, fn) { this._listeners.get(type)?.delete(fn); }
  listenerCount() { let n = 0; for (const s of this._listeners.values()) n += s.size; return n; }
  _fire(event) { for (const fn of [...(this._listeners.get(event.type) ?? [])]) fn.call(this, event); }
}

class FakeClassList {
  constructor() { this._set = new Set(); }
  add(...c) { c.forEach((x) => this._set.add(x)); }
  remove(...c) { c.forEach((x) => this._set.delete(x)); }
  toggle(c, force) {
    const on = force === undefined ? !this._set.has(c) : !!force;
    on ? this._set.add(c) : this._set.delete(c);
    return on;
  }
  contains(c) { return this._set.has(c); }
}

class FakeText {
  constructor(text) { this.nodeType = 3; this.data = String(text); this.parentNode = null; }
  get textContent() { return this.data; }
  set textContent(v) { this.data = String(v); }
  remove() { this.parentNode?.removeChild(this); }
}

class FakeElement extends Target {
  constructor(tag) {
    super();
    this.nodeType = 1;
    this.tagName = String(tag).toUpperCase();
    this.childNodes = [];
    this.parentNode = null;
    this.style = {};
    this.classList = new FakeClassList();
    this.dataset = {};
    this.attributes = {};
    Object.assign(this, { id: "", title: "", value: "", placeholder: "", tabIndex: -1, hidden: false, disabled: false, offsetWidth: 0 });
  }
  get children() { return this.childNodes.filter((c) => c.nodeType === 1); }
  get className() { return [...this.classList._set].join(" "); }
  set className(v) { this.classList = new FakeClassList(); String(v).split(/\s+/).filter(Boolean).forEach((c) => this.classList.add(c)); }
  get textContent() { return this.childNodes.map((c) => c.textContent).join(""); }
  set textContent(v) { this.replaceChildren(); if (v !== "" && v != null) this.appendChild(new FakeText(v)); }
  setAttribute(k, v) { this.attributes[k] = String(v); }
  getAttribute(k) { return this.attributes[k] ?? null; }
  appendChild(child) {
    child.parentNode?.removeChild(child);
    child.parentNode = this;
    this.childNodes.push(child);
    return child;
  }
  append(...nodes) { nodes.forEach((n) => this.appendChild(typeof n === "string" ? new FakeText(n) : n)); }
  removeChild(child) {
    const i = this.childNodes.indexOf(child);
    if (i >= 0) { this.childNodes.splice(i, 1); child.parentNode = null; }
    return child;
  }
  replaceChildren(...nodes) {
    for (const c of [...this.childNodes]) this.removeChild(c);
    this.append(...nodes);
  }
  remove() { this.parentNode?.removeChild(this); }
  contains(node) {
    for (let n = node; n; n = n.parentNode) if (n === this) return true;
    return false;
  }
  dispatchEvent(event) {
    if (!event.target) event.target = this;
    for (let n = this; n && !event.propagationStopped; n = n.parentNode) {
      event.currentTarget = n;
      n._fire?.(event);
    }
    return !event.defaultPrevented;
  }
  focus() { globalThis.document.activeElement = this; }
  blur() { if (globalThis.document.activeElement === this) globalThis.document.activeElement = globalThis.document.body; }
  select() {}
  scrollIntoView() {}
  getBoundingClientRect() { return { left: 0, top: 0, width: 0, height: 0, right: 0, bottom: 0 }; }
}

export function installFakeDom({ language = "fr-FR" } = {}) {
  const frames = new Map();
  let frameId = 0;
  const timers = new Map();
  let timerId = 0;
  let clock = 0;
  const observers = [];

  const doc = new Target();
  doc.head = new FakeElement("head");
  doc.body = new FakeElement("body");
  doc.hidden = false;
  doc.activeElement = doc.body;
  doc.createElement = (tag) => new FakeElement(tag);
  doc.createTextNode = (t) => new FakeText(t);
  doc.getElementById = (id) => {
    const walk = (n) => {
      if (n.nodeType !== 1) return null;
      if (n.id === id) return n;
      for (const c of n.childNodes) { const r = walk(c); if (r) return r; }
      return null;
    };
    return walk(doc.head) || walk(doc.body);
  };
  doc.dispatchEvent = (event) => { event.target ??= doc; doc._fire(event); return !event.defaultPrevented; };

  const store = new Map();
  class Observer {
    constructor(cb) { this.cb = cb; this.disconnected = false; observers.push(this); }
    observe() {}
    disconnect() { this.disconnected = true; }
  }

  Object.assign(globalThis, {
    document: doc,
    window: globalThis,
    localStorage: {
      getItem: (k) => (store.has(k) ? store.get(k) : null),
      setItem: (k, v) => store.set(k, String(v)),
      removeItem: (k) => store.delete(k),
    },
    ResizeObserver: class extends Observer {},
    IntersectionObserver: class extends Observer {},
    requestAnimationFrame: (fn) => { frames.set(++frameId, fn); return frameId; },
    cancelAnimationFrame: (id) => frames.delete(id),
    setTimeout: (fn, ms = 0) => { timers.set(++timerId, { fn, at: clock + ms, every: 0 }); return timerId; },
    clearTimeout: (id) => timers.delete(id),
    setInterval: (fn, ms = 0) => { timers.set(++timerId, { fn, at: clock + ms, every: Math.max(1, ms) }); return timerId; },
    clearInterval: (id) => timers.delete(id),
    Event: FakeEvent,
    WheelEvent: class extends FakeEvent {},
    KeyboardEvent: class extends FakeEvent {},
  });
  Object.defineProperty(globalThis, "navigator", { value: { language, clipboard: { writeText: async () => {} } }, configurable: true });
  Object.defineProperty(globalThis, "performance", { value: { now: () => clock }, configurable: true });

  return {
    flushFrames() {
      const list = [...frames.entries()];
      frames.clear();
      for (const [, fn] of list) fn(clock);
    },
    runTimers(ms) {
      const end = clock + ms;
      for (;;) {
        let next = null;
        for (const [id, t] of timers) if (t.at <= end && (!next || t.at < next[1].at || (t.at === next[1].at && id < next[0]))) next = [id, t];
        if (!next) break;
        const [id, t] = next;
        clock = t.at;
        if (t.every) t.at += t.every; else timers.delete(id);
        t.fn();
      }
      clock = end;
    },
    pendingTimers: () => timers.size,
    pendingFrames: () => frames.size,
    observers,
    docListeners: () => doc.listenerCount(),
  };
}
