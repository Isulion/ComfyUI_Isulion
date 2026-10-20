// Import a web/ extension with its ComfyUI imports pointed at comfy_stub.mjs.
import { readFile } from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const webDir = path.resolve(here, "../../web");

export async function loadExtension(name = "mega_prompt_v4") {
  const stubUrl = pathToFileURL(path.join(here, "comfy_stub.mjs")).href;
  let src = await readFile(path.join(webDir, `${name}.js`), "utf8");
  src = src
    .replaceAll('"../../scripts/app.js"', JSON.stringify(stubUrl))
    .replaceAll('"../../scripts/api.js"', JSON.stringify(stubUrl))
    .replaceAll('"./mega_prompt_v4_core.js"', JSON.stringify(pathToFileURL(path.join(webDir, "mega_prompt_v4_core.js")).href));
  await import("data:text/javascript;charset=utf-8," + encodeURIComponent(src));
  return import(stubUrl);
}
