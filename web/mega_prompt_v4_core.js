// Pure helpers for the Mega Prompt V4 cabinet (no DOM access, no registerExtension):
// imported by mega_prompt_v4.js and by the Node test harness.

export const REELS = ["theme", "subject", "location", "style", "effects"];
export const ROLL_REELS = REELS.slice(1);
const COMPLEXITIES = ["simple", "detailed", "complex"];

export function defaultState() {
  return {
    version: 1,
    theme: { name: "", locked: false },
    reels: {
      subject: { text: "", locked: false, custom: "" },
      location: { text: "", locked: false, custom: "", enabled: true },
      style: { text: "", locked: false, enabled: true },
      effects: { text: "", locked: false, enabled: true },
    },
    complexity: "detailed",
    lora: "",
    frozen_prompt: "",
  };
}

const str = (v) => (typeof v === "string" ? v : "");
const bool = (v, d) => (typeof v === "boolean" ? v : d);
const obj = (v) => (v && typeof v === "object" && !Array.isArray(v) ? v : {});

// Same contract as parse_state() in Core_Nodes/mega_prompt_v4.py
export function readState(raw) {
  let data = raw;
  if (typeof raw === "string") {
    try { data = JSON.parse(raw); } catch { data = null; }
  }
  const state = defaultState();
  if (!data || typeof data !== "object" || Array.isArray(data) || data.version !== 1) return state;
  const theme = obj(data.theme);
  state.theme = { name: str(theme.name), locked: bool(theme.locked, false) };
  const reels = obj(data.reels);
  for (const [name, reel] of Object.entries(state.reels)) {
    const src = obj(reels[name]);
    reel.text = str(src.text);
    reel.locked = bool(src.locked, false);
    if ("custom" in reel) reel.custom = str(src.custom);
    if ("enabled" in reel) reel.enabled = bool(src.enabled, true);
  }
  state.complexity = COMPLEXITIES.includes(data.complexity) ? data.complexity : "detailed";
  state.lora = str(data.lora);
  state.frozen_prompt = str(data.frozen_prompt);
  return state;
}

// Short label for a reel window: first whole words of a long generated component
export function shortText(text, max = 22) {
  const words = String(text ?? "").replace(/[()]/g, "").replace(/\s+/g, " ").trim().split(" ").filter(Boolean);
  if (!words.length) return "—";
  if (words[0].length > max) return words[0].slice(0, max - 1) + "…";
  let out = words[0];
  for (const w of words.slice(1)) {
    if (out.length + 1 + w.length > max) break;
    out += " " + w;
  }
  return out;
}

export function pickLang(navLang, stored) {
  if (stored === "fr" || stored === "en") return stored;
  return String(navLang ?? "").toLowerCase().startsWith("fr") ? "fr" : "en";
}

export function historyRows(history, max = 5) {
  const favs = history.filter((h) => h.fav);
  const rest = history.filter((h) => !h.fav);
  return [...favs, ...rest].slice(0, max);
}

export const TEXT = {
  en: {
    marquee: "PROMPT JACKPOT",
    reels: { theme: "THEME", subject: "SUBJECT", location: "PLACE", style: "STYLE", effects: "EFFECTS" },
    pull: "PULL",
    complexity: { simple: "SIMPLE", detailed: "DETAILED", complex: "COMPLEX" },
    lora: "LoRA",
    promptTitle: "> PROMPT",
    copy: "📋 COPY",
    copied: "✅ COPIED",
    edit: "✏️ EDIT",
    ok: "OK",
    cancel: "CANCEL",
    frozenBadge: "❄ FROZEN PROMPT",
    history: "> LAST DRAWS",
    draw: "DRAW #",
    seed: "SEED ",
    searchPlaceholder: "🔍 search a theme…",
    editPlaceholder: "your own text (Enter = OK, Esc = cancel)",
    emptyHint: "Pull the lever or queue the workflow!",
    error: "ERROR",
    help: {
      title: "HOW TO PLAY",
      close: "✕",
      sections: [
        ["What is it?", "A slot machine that writes your prompt. Each reel draws one part (theme, subject, place, style, effects) from the Isulion themes. The node outputs a single text: the prompt."],
        ["The lever", "PULL re-draws every unlocked reel right in the browser, without running the workflow, so you can explore."],
        ["On every run", "Each time the workflow runs, the machine spins again: unlocked reels get a new draw, and the screen shows exactly the prompt that was sent."],
        ["🔒 Lock", "A locked reel never moves, neither with the lever nor when the workflow runs. Click again to unlock."],
        ["◀ ▶ 🔍 Theme", "Browse themes one by one or search them all. Picking a theme locks it and re-draws the other unlocked reels in that theme. Leave the theme unlocked to get a random theme each time."],
        ["✏️ Your own text", "On SUBJECT and PLACE, type your own text. It stays on every draw while the theme rebuilds the wording around it. Clear it with ✕ to go back to random."],
        ["👁 / 🚫 On-off", "PLACE, STYLE and EFFECTS can be switched off: they turn grey and leave the prompt."],
        ["Complexity", "SIMPLE drops quality boilerplate, DETAILED adds a few detail words, COMPLEX adds a richer block (composition, textures, lighting)."],
        ["LoRA", "Fixed text always added at the end of the prompt, e.g. a trigger word or <lora:name:0.8>."],
        ["PROMPT screen", "Click a coloured piece to re-draw only that reel. COPY puts the prompt in the clipboard. EDIT freezes a hand-written prompt: it is output as-is on every run until you pull the lever."],
        ["Last draws", "The last five draws, one per line. Click a line to load it back into the machine; ☆ keeps it as a favourite, shown on top."],
      ],
    },
  },
  fr: {
    marquee: "PROMPT JACKPOT",
    reels: { theme: "THÈME", subject: "SUJET", location: "LIEU", style: "STYLE", effects: "EFFETS" },
    pull: "TIRER",
    complexity: { simple: "SIMPLE", detailed: "DÉTAILLÉ", complex: "COMPLEXE" },
    lora: "LoRA",
    promptTitle: "> PROMPT",
    copy: "📋 COPIER",
    copied: "✅ COPIÉ",
    edit: "✏️ ÉDITER",
    ok: "OK",
    cancel: "ANNULER",
    frozenBadge: "❄ PROMPT FIGÉ",
    history: "> DERNIERS TIRAGES",
    draw: "TIRAGE #",
    seed: "GRAINE ",
    searchPlaceholder: "🔍 chercher un thème…",
    editPlaceholder: "ton texte (Entrée = OK, Échap = annuler)",
    emptyHint: "Tire le levier ou lance le workflow !",
    error: "ERREUR",
    help: {
      title: "COMMENT JOUER",
      close: "✕",
      sections: [
        ["C'est quoi ?", "Une machine à sous qui écrit ton prompt. Chaque rouleau tire un morceau (thème, sujet, lieu, style, effets) dans les thèmes Isulion. Le node sort un seul texte : le prompt."],
        ["Le levier", "TIRER relance tous les rouleaux non verrouillés directement dans le navigateur, sans lancer le workflow, pour explorer."],
        ["À chaque exécution", "À chaque lancement du workflow, la machine retourne : les rouleaux non verrouillés sont tirés à nouveau, et l'écran affiche exactement le prompt envoyé."],
        ["🔒 Verrou", "Un rouleau verrouillé ne bouge plus, ni avec le levier ni à l'exécution. Clique à nouveau pour le libérer."],
        ["◀ ▶ 🔍 Thème", "Fais défiler les thèmes un par un ou cherche parmi tous. Choisir un thème le verrouille et relance les autres rouleaux libres dans ce thème. Laisse le thème déverrouillé pour un thème au hasard à chaque fois."],
        ["✏️ Ton texte", "Sur SUJET et LIEU, tape ton propre texte. Il reste à chaque tirage, et le thème reconstruit la formulation autour. Efface-le avec ✕ pour revenir au hasard."],
        ["👁 / 🚫 Allumer, éteindre", "LIEU, STYLE et EFFETS peuvent être éteints : ils passent en gris et sortent du prompt."],
        ["Complexité", "SIMPLE retire les formules de qualité, DÉTAILLÉ ajoute quelques mots de détail, COMPLEXE ajoute un bloc plus riche (composition, textures, lumière)."],
        ["LoRA", "Texte fixe toujours ajouté en fin de prompt, par exemple un mot déclencheur ou <lora:nom:0.8>."],
        ["Écran PROMPT", "Clique un morceau coloré pour relancer seulement ce rouleau. COPIER met le prompt dans le presse-papiers. ÉDITER fige un prompt écrit à la main : il sort tel quel à chaque exécution jusqu'au prochain coup de levier."],
        ["Derniers tirages", "Les cinq derniers tirages, un par ligne. Clique une ligne pour la recharger dans la machine ; ☆ la garde en favori, affiché en tête."],
      ],
    },
  },
};
