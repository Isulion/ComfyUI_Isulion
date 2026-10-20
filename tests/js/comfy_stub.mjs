// Stand-in for ComfyUI's scripts/app.js and scripts/api.js in the Node harness.
export const app = {
  extensions: [],
  registerExtension(ext) { app.extensions.push(ext); },
  canvas: { canvas: { dispatchEvent() {} } },
  graph: { getNodeById() { return null; } },
};

export const api = {
  calls: [],
  responders: {},
  async fetchApi(route, opts = {}) {
    const body = opts.body ? JSON.parse(opts.body) : null;
    this.calls.push({ route, opts, body });
    let value = this.responders[route];
    if (typeof value === "function") value = value(body);
    value = await value;
    const status = value && value.__status ? value.__status : 200;
    return { ok: status < 400, status, json: async () => value };
  },
};
