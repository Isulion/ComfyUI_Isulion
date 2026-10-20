# Mega Prompt V4 « Prompt Jackpot » — plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Objectif :** un node `IsulionMegaPromptV4` (« 🕹️ Isulion Mega Prompt V4 ») qui tire un prompt à partir des 109 thèmes existants, présenté comme une borne d'arcade / machine à sous dans un DOM widget, avec une seule sortie `prompt`.

**Architecture :** le Python (`Core_Nodes/mega_prompt_v4.py`) possède toute la logique : parsing d'un état JSON versionné, tirage pur `roll(state, reels, seed)` qui n'appelle les handlers V3 que sous un verrou partagé avec la V3, assemblage du prompt en segments. Deux routes aiohttp (`themes`, `roll`) exposent cette même fonction au navigateur ; l'exécution du workflow l'appelle aussi et renvoie le résultat dans `ui.draw`. Le JS (`web/mega_prompt_v4.js` + `web/mega_prompt_v4_core.js`) n'assemble jamais : il édite l'état, l'écrit dans le widget caché `machine_state`, affiche les segments reçus et anime.

**Stack :** Python 3.10+ (stdlib seulement, aiohttp/PromptServer fournis par ComfyUI), JavaScript ES module (LiteGraph/ComfyUI frontend), tests Python via `python3 tests/run_all.py`, tests JS via `node tests/js/test_mega_prompt_v4.mjs` (Node 22, aucune dépendance npm).

**Spec :** `docs/superpowers/specs/2026-10-20-megaprompt-v4-design.md` (lire aussi `/home/moi/.claude/skills/comfyui-supernodes/SKILL.md` et `reference.md` §2, 3, 4, 6, 9, 10, 12 ; maquette `.superpowers/brainstorm/1944405-1792518362/content/arcade-full-v2.html`).

## Contraintes globales

- Python 3.10+, aucune nouvelle dépendance ; `aiohttp` et `server` n'existent pas dans l'environnement de test : tout import de ces modules est gardé par `try/except ImportError`, la logique des routes reste dans des fonctions pures.
- `pytest` n'est pas installé : point d'entrée `python3 tests/run_all.py`, chaque nouveau module de test est ajouté à `MODULES`. Les tests importent le paquet via `isulion_testkit.import_package()` puis `from isulion_pkg.Core_Nodes import ...`.
- Ne pas modifier le comportement ni le contrat de la V3 (seul ajout : `with GENERATION_LOCK:` autour de `set_seed` + `handler.generate`). « 🎲 Dynamic Random » reste dans le registre V3 (fixture `theme_display_names.json` inchangée).
- Node : clé `IsulionMegaPromptV4`, affichage `🕹️ Isulion Mega Prompt V4`, `CATEGORY = "Isulion/Core"`, `RETURN_TYPES = ("STRING",)`, `RETURN_NAMES = ("prompt",)`, `OUTPUT_NODE = True`, `IS_CHANGED` → `float("nan")`.
- `INPUT_TYPES` n'expose que `{"required": {"machine_state": ("STRING", {"default": '{"version": 1}'})}}` : pas de liste de thèmes, pas de `unique_id`.
- Routes : `GET /isulion/megaprompt_v4/themes`, `POST /isulion/megaprompt_v4/roll`.
- `__init__.py` est en CRLF (`grep -c $'\r' __init__.py` = `wc -l`) : préserver ; les fixtures JSON sont en LF.
- JS : imports `"../../scripts/app.js"` et `"../../scripts/api.js"` ; DOM widget `{serialize:false, hideOnZoom:false, getMinHeight}` ; widget `machine_state` masqué par `hidden=true` + `type="converted-widget"`, jamais `serialize:false` ; après chaque modification `w.value=…; w.callback?.(v); node.graph?.change(); node.setDirtyCanvas(true,true)` ; classes CSS préfixées `isu-mpv4-` ; aucun `innerHTML`, aucun `querySelector` (les éléments sont construits par un helper et gardés en référence, ce qui rend le faux DOM trivial) ; pas de `window.prompt`.
- Animations CSS mises en pause par la classe `isu-mpv4-paused` (IntersectionObserver + `visibilitychange`) ; aucun `setDirtyCanvas` en boucle.
- Branche `feat/megaprompt-v4` ; chaque commit se termine par la ligne `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Identifiants de code en anglais ; textes de l'interface dans le dictionnaire `TEXT = {en, fr}`.

## Points de vigilance (Review Focus)

1. Un handler de thème qui lève une exception pendant `generate` (données de config manquantes) : le node ne doit pas faire échouer la file ; le prompt renvoyé commence par `Error:` et l'état n'est pas modifié. → test `test_roll_handler_exception_returns_error_prompt` (Tâche 4).
2. Une réponse `roll` tardive qui arrive après un `onExecuted` (levier tiré juste avant Queue) : c'est le résultat du serveur qui doit rester à l'écran. → test `late roll response is ignored after onExecuted` (Tâche 8).
3. Un workflow sauvegardé avec un thème qui n'existe plus dans le registre : tirage sur un thème au hasard, sans exception, et le nouveau nom est écrit dans l'état. → test `test_roll_unknown_theme_falls_back_to_random` (Tâche 4).
4. Un texte perso qui contient des virgules et des parenthèses (`"my elf queen, ((8k))"`) : il doit survivre au dédoublonnage et au mode SIMPLE (seuls les blocs de qualité exacts sont retirés). → test `test_assemble_simple_keeps_custom_text_chunks` (Tâche 3).
5. Un rouleau éteint puis rallumé : il ne doit pas rester vide ; le tirage suivant qui le demande le remplit. → test `test_roll_disabled_reel_keeps_text_then_fills_when_enabled` (Tâche 4).

---

## Structure des fichiers

| Fichier | Rôle |
|---|---|
| `Core_Nodes/mega_prompt_V3.py` (modif.) | ajoute `GENERATION_LOCK` et l'utilise dans `generate` |
| `Core_Nodes/mega_prompt_v4.py` (créé) | état, assemblage, tirage pur, classe du node |
| `Core_Nodes/mega_prompt_v4_routes.py` (créé) | `themes_payload`, `roll_payload`, `register_routes` (aiohttp optionnel) |
| `__init__.py` (modif., CRLF) | import, mappings, import du module de routes |
| `tests/test_mega_prompt_v4.py` (créé) | tests Python |
| `tests/test_mega_prompt_v4_js.py` (créé) | lance `node --check` + le harnais JS depuis `run_all.py` (skip si `node` absent) |
| `tests/fixtures/expected_node_keys.json`, `node_contracts_v2.json`, `tests/run_all.py` (modif.) | enregistrement |
| `web/mega_prompt_v4_core.js` (créé) | fonctions pures sans DOM : `readState`, `shortText`, `pickLang`, `historyRows`, `TEXT` |
| `web/mega_prompt_v4.js` (créé) | extension : classe `PromptJackpot`, CSS, hooks du node |
| `tests/js/fake_dom.mjs`, `tests/js/comfy_stub.mjs`, `tests/js/load_extension.mjs`, `tests/js/test_mega_prompt_v4.mjs` (créés) | harnais Node |

### Formes de données partagées (référence pour toutes les tâches)

État `machine_state` v1 (Python `default_state()` et JS `readState` produisent la même chose) :

```json
{"version": 1,
 "theme": {"name": "", "locked": false},
 "reels": {
   "subject":  {"text": "", "locked": false, "custom": ""},
   "location": {"text": "", "locked": false, "custom": "", "enabled": true},
   "style":    {"text": "", "locked": false, "enabled": true},
   "effects":  {"text": "", "locked": false, "enabled": true}},
 "complexity": "detailed",
 "lora": "",
 "frozen_prompt": ""}
```

Résultat de tirage (`RollResult`, renvoyé par `roll()`, par `POST roll` et dans `ui.draw[0]`) :

```json
{"state": {"...état v1, theme.name résolu..."},
 "prompt": "texte final",
 "segments": [{"reel": "subject|location|style|effects|complexity|lora|frozen|error", "text": "..."}],
 "rolled": ["subject", "style"],
 "seed": 482913,
 "theme": {"name": "anime", "display": "🎌 Anime", "icon": "🎌", "label": "Anime"}}
```

`node.properties.isu_mpv4` (affichage seulement) : `{"draws": 0, "seed": null, "history": [{"payload": RollResult, "fav": false}], "last": RollResult|null}`.

---

### Tâche 0 : branche et travail en attente

**Files:** aucun fichier nouveau.

Le dépôt contient le node Space Invaders non commité (`__init__.py`, `tests/fixtures/*.json`, `tests/run_all.py`, `Core_Nodes/space_invaders_node.py`, `tests/test_space_invaders.py`, `web/space_invaders.js`) qui touche les mêmes fichiers que ce plan. Il est terminé et testé (53/53) : on le commet seul, d'abord, pour que les commits V4 restent lisibles.

- [ ] **Step 1 : créer la branche**

Run: `git checkout -b feat/megaprompt-v4`

- [ ] **Step 2 : vérifier que la suite passe avant tout changement**

Run: `python3 tests/run_all.py | tail -3`
Expected: `SUMMARY: 53/53 passed, 0 failed`

- [ ] **Step 3 : commettre le travail Space Invaders en attente (sans `.superpowers/`)**

```bash
git add __init__.py tests/fixtures/expected_node_keys.json tests/fixtures/node_contracts_v2.json tests/run_all.py Core_Nodes/space_invaders_node.py tests/test_space_invaders.py web/space_invaders.js
git commit -m "feat: Space Invaders node (DOM widget game, hidden state widget)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

- [ ] **Step 4 : commettre la spec et ce plan**

```bash
git add docs/superpowers/specs/2026-10-20-megaprompt-v4-design.md docs/superpowers/plans/2026-10-20-megaprompt-v4.md
git commit -m "docs: Mega Prompt V4 design spec and implementation plan

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 1 : verrou de génération partagé dans la V3

**Files:**
- Modify: `Core_Nodes/mega_prompt_V3.py:163-176` (à côté de `get_theme_registry`) et `:261-315` (`generate`)
- Test: `tests/test_theme_registry.py`

**Interfaces:**
- Produces: `GENERATION_LOCK: threading.Lock` (module-level dans `mega_prompt_V3.py`). Toute séquence `config_manager.set_seed(seed)` + `handler.generate(...)` s'exécute sous `with GENERATION_LOCK:`.

- [ ] **Step 1 : écrire le test**

Ajouter à `tests/test_theme_registry.py` :

```python
def test_v3_generate_runs_under_the_shared_generation_lock():
    import_package()
    from isulion_pkg.Core_Nodes import mega_prompt_V3 as v3

    class RecordingLock:
        def __init__(self): self.entries = 0
        def __enter__(self): self.entries += 1
        def __exit__(self, *a): return False

    original, v3.GENERATION_LOCK = v3.GENERATION_LOCK, RecordingLock()
    try:
        v3.IsulionMegaPromptV3().generate(theme=ANIME_THEME, seed=1)
        assert v3.GENERATION_LOCK.entries == 1
    finally:
        v3.GENERATION_LOCK = original
```

- [ ] **Step 2 : vérifier l'échec**

Run: `python3 tests/run_all.py 2>&1 | grep -A3 "FAIL test_v3_generate"`
Expected: `FAIL` avec `AttributeError: ... has no attribute 'GENERATION_LOCK'`

- [ ] **Step 3 : implémenter**

Dans `mega_prompt_V3.py` : `import threading` ; juste avant `get_theme_registry` : `GENERATION_LOCK = threading.Lock()` avec un commentaire (RNG partagé `ConfigManager.random`, routes V4 concurrentes). Dans `generate`, déplacer `self.config_manager.set_seed(seed)` à côté de l'appel `handler.generate(...)` et envelopper les deux dans `with GENERATION_LOCK:` (le verrou est lu comme global du module, pas capturé à l'import, pour rester remplaçable). Rien d'autre ne change.

- [ ] **Step 4 : vérifier**

Run: `python3 tests/run_all.py | tail -3`
Expected: `SUMMARY: 54/54 passed, 0 failed`

- [ ] **Step 5 : commit**

```bash
git add Core_Nodes/mega_prompt_V3.py tests/test_theme_registry.py
git commit -m "refactor(megaprompt-v3): guard seed+generate with a shared GENERATION_LOCK

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 2 : état V4 et liste des thèmes

**Files:**
- Create: `Core_Nodes/mega_prompt_v4.py`
- Create: `tests/test_mega_prompt_v4.py`
- Modify: `tests/run_all.py:23-34` (ajouter `"test_mega_prompt_v4"` après `"test_space_invaders"`)

**Interfaces:**
- Consumes: `get_theme_registry()` de `mega_prompt_V3` (`registry.handlers: dict[str, BaseThemeHandler]`, `registry.config_manager`, chaque handler a `DISPLAY_NAME`).
- Produces (dans `mega_prompt_v4.py`) :
  - `REEL_NAMES = ("theme", "subject", "location", "style", "effects")`, `COMPLEXITIES = ("simple", "detailed", "complex")`, `DEFAULT_STATE = '{"version": 1}'`, `STATE_VERSION = 1`
  - `default_state() -> dict` (forme v1 ci-dessus, `theme.name == ""`)
  - `parse_state(raw) -> dict` : accepte `str` JSON, `dict`, ou `None` ; toute entrée invalide, non-dict, ou de `version != 1` → `default_state()` ; chaque champ est coercé : `locked`/`enabled` → `bool` strict (sinon défaut), `text`/`custom`/`lora`/`frozen_prompt`/`theme.name` → `str` (sinon `""`), `complexity` hors de `COMPLEXITIES` → `"detailed"` ; clés inconnues ignorées ; renvoie toujours un dict neuf complet.
  - `theme_entry(name: str, registry=None) -> dict` : `{"name", "display", "icon", "label"}` ; `display = handler.DISPLAY_NAME` ; `icon, _, label = display.partition(" ")` ; si `label == ""` → `icon = "🎰"`, `label = display` ; nom inconnu → `{"name": name, "display": name, "icon": "🎰", "label": name}`.
  - `list_themes(registry=None) -> list[dict]` : un `theme_entry` par handler, trié par `label` (même clé que V3 : `display.split(" ", 1)[-1].strip()`), sans « random ».

- [ ] **Step 1 : écrire les tests**

```python
"""Checks for the Isulion Mega Prompt V4 node (Python side of web/mega_prompt_v4.js)."""
import json
from isulion_testkit import import_package

def _mp4():
    import_package()
    from isulion_pkg.Core_Nodes import mega_prompt_v4 as mp4
    return mp4

def test_default_state_shape():
    s = _mp4().default_state()
    assert s["version"] == 1 and s["theme"] == {"name": "", "locked": False}
    assert set(s["reels"]) == {"subject", "location", "style", "effects"}
    assert s["reels"]["location"] == {"text": "", "locked": False, "custom": "", "enabled": True}
    assert "enabled" not in s["reels"]["subject"] and "custom" not in s["reels"]["style"]
    assert (s["complexity"], s["lora"], s["frozen_prompt"]) == ("detailed", "", "")

def test_parse_state_falls_back_on_bad_input():
    mp4 = _mp4()
    for raw in (None, "", "not json", "[1]", '{"version": 2}', '{"version": "1"}', 7):
        assert mp4.parse_state(raw) == mp4.default_state(), raw

def test_parse_state_keeps_valid_fields_and_coerces_bad_ones():
    mp4 = _mp4()
    s = mp4.parse_state(json.dumps({"version": 1, "theme": {"name": "anime", "locked": 1},
        "reels": {"subject": {"text": "hero", "locked": True, "custom": 5},
                  "style": {"enabled": "no", "text": None}},
        "complexity": "epic", "lora": ["x"], "frozen_prompt": "fixed", "junk": 1}))
    assert s["theme"] == {"name": "anime", "locked": False}
    assert s["reels"]["subject"] == {"text": "hero", "locked": True, "custom": ""}
    assert s["reels"]["style"] == {"text": "", "locked": False, "enabled": True}
    assert s["reels"]["location"]["enabled"] is True
    assert (s["complexity"], s["lora"], s["frozen_prompt"]) == ("detailed", "", "fixed")
    assert "junk" not in s
    assert mp4.parse_state(mp4.DEFAULT_STATE) == mp4.default_state()

def test_theme_entry_and_list_themes():
    mp4 = _mp4()
    assert mp4.theme_entry("anime") == {"name": "anime", "display": "🎌 Anime", "icon": "🎌", "label": "Anime"}
    assert mp4.theme_entry("nope") == {"name": "nope", "display": "nope", "icon": "🎰", "label": "nope"}
    themes = mp4.list_themes()
    names = [t["name"] for t in themes]
    assert "random" not in names and "anime" in names and len(names) == len(set(names))
    assert [t["label"] for t in themes] == sorted(t["label"] for t in themes)
```

- [ ] **Step 2 : ajouter le module à `run_all.py` et vérifier l'échec**

Run: `python3 tests/run_all.py 2>&1 | grep -c "FAIL\|ModuleNotFoundError"`
Expected: un échec d'import (`ModuleNotFoundError: ... mega_prompt_v4`) — le runner s'arrête sur l'import du module de test.

- [ ] **Step 3 : implémenter les constantes, `default_state`, `parse_state`, `theme_entry`, `list_themes` dans `Core_Nodes/mega_prompt_v4.py`**

Imports : `json, random, logging, threading`-free (le verrou vient de V3 : `from .mega_prompt_V3 import get_theme_registry, deduplicate_prompt_parts, GENERATION_LOCK`). Un `bool` strict se teste par `isinstance(v, bool)` (et pas `int`), comme dans `space_invaders_node.py`.

- [ ] **Step 4 : vérifier**

Run: `python3 tests/run_all.py | tail -3`
Expected: `SUMMARY: 58/58 passed, 0 failed`

- [ ] **Step 5 : commit**

```bash
git add Core_Nodes/mega_prompt_v4.py tests/test_mega_prompt_v4.py tests/run_all.py
git commit -m "feat(megaprompt-v4): versioned machine state parsing and theme listing

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 3 : assemblage du prompt

**Files:**
- Modify: `Core_Nodes/mega_prompt_v4.py`
- Test: `tests/test_mega_prompt_v4.py`

**Interfaces:**
- Produces :
  - `COMPLEXITY_SUFFIX = {"simple": "", "detailed": "highly detailed, sharp focus", "complex": "highly detailed, intricate textures, cinematic composition, dramatic lighting, masterpiece"}`
  - `SIMPLE_DROP = frozenset({"masterpiece", "best quality", "highly detailed", "ultra detailed", "artistic excellence", "professional quality", "8k", "4k", "8k resolution"})`
  - `simplify_component(text: str) -> str` : découpe sur `","`, pour chaque morceau `key = chunk.strip().strip("()").strip().lower()` ; retire le morceau si `key in SIMPLE_DROP` ; rejoint par `", "` les morceaux restants non vides.
  - `assemble_prompt(state: dict) -> tuple[str, list[dict]]` : segments dans l'ordre `subject` (si `text` non vide), `location`/`style`/`effects` (si `enabled` et `text` non vide) ; en `simple` chaque texte passe par `simplify_component` ; puis segment `complexity` = `COMPLEXITY_SUFFIX[complexity]` s'il est non vide ; puis segment `lora` = `lora.strip()` s'il est non vide ; dédoublonnage des segments par `text.strip().lower()` (premier gardé, comme `deduplicate_prompt_parts`) ; `prompt = ", ".join(seg["text"] for seg in segments)`. Si `frozen_prompt.strip()` est non vide : renvoie `(frozen_prompt, [{"reel": "frozen", "text": frozen_prompt}])`.

- [ ] **Step 1 : écrire les tests**

```python
def _state(**over):
    mp4 = _mp4()
    s = mp4.default_state()
    s["reels"]["subject"]["text"] = "a hero, ((masterpiece))"
    s["reels"]["location"]["text"] = "in a forest"
    s["reels"]["style"]["text"] = "oil painting"
    s["reels"]["effects"]["text"] = "glowing embers"
    for k, v in over.items(): s[k] = v
    return s

def test_assemble_order_complexity_and_lora():
    mp4 = _mp4()
    s = _state(lora="  <lora:jade:0.8> ")
    prompt, segs = mp4.assemble_prompt(s)
    assert [x["reel"] for x in segs] == ["subject", "location", "style", "effects", "complexity", "lora"]
    assert prompt == "a hero, ((masterpiece)), in a forest, oil painting, glowing embers, highly detailed, sharp focus, <lora:jade:0.8>"
    assert prompt.endswith("<lora:jade:0.8>")

def test_assemble_disabled_reel_is_absent():
    mp4 = _mp4()
    s = _state()
    s["reels"]["style"]["enabled"] = False
    prompt, segs = mp4.assemble_prompt(s)
    assert "oil painting" not in prompt and "style" not in [x["reel"] for x in segs]

def test_assemble_simple_keeps_custom_text_chunks():
    mp4 = _mp4()
    s = _state(complexity="simple")
    s["reels"]["subject"]["text"] = "my elf queen, ((8k)), (queen of 8 kingdoms)"
    prompt, segs = mp4.assemble_prompt(s)
    assert segs[0]["text"] == "my elf queen, (queen of 8 kingdoms)"
    assert "complexity" not in [x["reel"] for x in segs]

def test_assemble_complex_and_dedup():
    mp4 = _mp4()
    s = _state(complexity="complex")
    s["reels"]["effects"]["text"] = "Oil Painting"
    prompt, segs = mp4.assemble_prompt(s)
    assert prompt.count("il painting") == 1 and prompt.endswith("masterpiece")

def test_assemble_frozen_prompt_wins():
    mp4 = _mp4()
    prompt, segs = mp4.assemble_prompt(_state(frozen_prompt="exactly this", lora="x"))
    assert prompt == "exactly this" and segs == [{"reel": "frozen", "text": "exactly this"}]
```

- [ ] **Step 2 : vérifier l'échec**

Run: `python3 tests/run_all.py 2>&1 | grep "FAIL test_assemble" | wc -l`
Expected: `5`

- [ ] **Step 3 : implémenter `COMPLEXITY_SUFFIX`, `SIMPLE_DROP`, `simplify_component`, `assemble_prompt`**

- [ ] **Step 4 : vérifier**

Run: `python3 tests/run_all.py | tail -3`
Expected: `SUMMARY: 63/63 passed, 0 failed`

- [ ] **Step 5 : commit**

```bash
git add Core_Nodes/mega_prompt_v4.py tests/test_mega_prompt_v4.py
git commit -m "feat(megaprompt-v4): prompt assembly with complexity, LoRA and frozen prompt

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 4 : tirage pur `roll`

**Files:**
- Modify: `Core_Nodes/mega_prompt_v4.py`
- Test: `tests/test_mega_prompt_v4.py`

**Interfaces:**
- Consumes: `GENERATION_LOCK` (Tâche 1), `parse_state`/`theme_entry` (Tâche 2), `assemble_prompt` (Tâche 3).
- Produces :
  - `new_seed() -> int` : `random.SystemRandom().randrange(0, 2**32)`.
  - `COMPONENT_KEYS = {"subject": "subject", "location": "environment", "style": "style", "effects": "effects"}`.
  - `roll(state: dict, reels, seed: int, registry=None) -> dict` (`RollResult`). `registry` défaut `get_theme_registry()`. Algorithme :
    1. `state = parse_state(state)` (copie neuve) ; `reels = set(reels) & set(REEL_NAMES)`.
    2. Si `state["frozen_prompt"].strip()` : `prompt, segments = assemble_prompt(state)` ; renvoie avec `rolled=[]`, `theme=theme_entry(state["theme"]["name"], registry)`.
    3. `rng = random.Random(seed)` ; `names = sorted(registry.handlers)` ; si `"theme" in reels and not theme.locked`, ou si `theme.name not in registry.handlers` : `theme.name = rng.choice(names)` et `"theme"` est compté dans `rolled`.
    4. `to_roll = [r for r in ("subject","location","style","effects") if r in reels and not locked and reels[r].get("enabled", True)]`.
    5. Si `to_roll` : `with GENERATION_LOCK: registry.config_manager.set_seed(seed); components = handler.generate(custom_subject=subject.custom, custom_location=location.custom, include_environment=location.enabled, include_style=style.enabled, include_effects=effects.enabled)` ; pour chaque `r in to_roll` : `reels[r]["text"] = str(components.get(COMPONENT_KEYS[r]) or "")` (un `components` non-dict compte comme `{}`). Une exception du handler (sauf `KeyboardInterrupt`) est journalisée et renvoie `{"state": état d'entrée parsé, "prompt": f"Error: {type(e).__name__}: {e}", "segments": [{"reel": "error", "text": …}], "rolled": [], "seed": seed, "theme": …}`.
    6. `prompt, segments = assemble_prompt(state)` ; `rolled = (["theme"] si tiré) + to_roll`.

- [ ] **Step 1 : écrire les tests**

```python
import random, types

class _Handler:
    DISPLAY_NAME = "🧪 Alpha"
    def __init__(self, fail=False): self.calls, self.fail = [], fail
    def generate(self, **kw):
        self.calls.append(kw)
        if self.fail: raise KeyError("anime.characters")
        n = len(self.calls)
        return {"subject": f"subject {kw['custom_subject'] or n}", "environment": f"env {kw['custom_location'] or n}",
                "style": f"style {n}", "effects": f"fx {n}"}

def _registry(fail=False):
    h = _Handler(fail)
    cm = types.SimpleNamespace(random=random.Random(), seeds=[])
    cm.set_seed = cm.seeds.append
    return types.SimpleNamespace(handlers={"alpha": h, "beta": _Handler()}, config_manager=cm), h

def test_roll_same_seed_same_result_with_real_registry():
    mp4 = _mp4()
    s = mp4.default_state(); s["theme"] = {"name": "anime", "locked": True}
    a, b = mp4.roll(s, mp4.REEL_NAMES, 42), mp4.roll(s, mp4.REEL_NAMES, 42)
    assert a == b and a["prompt"] and a["seed"] == 42 and a["theme"]["name"] == "anime"
    assert a["state"]["theme"]["name"] == "anime" and "theme" not in a["rolled"]
    assert mp4.roll(s, mp4.REEL_NAMES, 43)["prompt"] != a["prompt"]

def test_roll_never_touches_locked_reels_and_only_requested_ones():
    mp4 = _mp4()
    reg, h = _registry()
    s = mp4.default_state(); s["theme"] = {"name": "alpha", "locked": True}
    s["reels"]["subject"].update(text="KEEP ME", locked=True)
    s["reels"]["style"]["text"] = "old style"
    out = mp4.roll(s, ["subject", "location"], 1, registry=reg)
    r = out["state"]["reels"]
    assert r["subject"]["text"] == "KEEP ME" and r["style"]["text"] == "old style"
    assert r["location"]["text"] == "env 1" and out["rolled"] == ["location"]
    assert reg.config_manager.seeds == [1] and h.calls[0]["include_style"] is True
    assert s["reels"]["location"]["text"] == ""  # input not mutated

def test_roll_unlocked_theme_is_random_and_recorded():
    mp4 = _mp4()
    reg, _ = _registry()
    s = mp4.default_state()
    out = mp4.roll(s, mp4.REEL_NAMES, 7, registry=reg)
    assert out["state"]["theme"]["name"] in ("alpha", "beta") and "theme" in out["rolled"]
    assert out["theme"]["icon"] == "🧪"

def test_roll_unknown_theme_falls_back_to_random():
    mp4 = _mp4()
    reg, _ = _registry()
    s = mp4.default_state(); s["theme"] = {"name": "gone", "locked": True}
    out = mp4.roll(s, ["style"], 3, registry=reg)
    assert out["state"]["theme"]["name"] in ("alpha", "beta") and out["prompt"]

def test_roll_pinned_custom_text_is_passed_to_handler():
    mp4 = _mp4()
    reg, h = _registry()
    s = mp4.default_state(); s["theme"] = {"name": "alpha", "locked": True}
    s["reels"]["subject"]["custom"] = "my elf queen"
    out = mp4.roll(s, mp4.REEL_NAMES, 1, registry=reg)
    assert h.calls[0]["custom_subject"] == "my elf queen"
    assert out["state"]["reels"]["subject"]["text"] == "subject my elf queen"

def test_roll_disabled_reel_keeps_text_then_fills_when_enabled():
    mp4 = _mp4()
    reg, h = _registry()
    s = mp4.default_state(); s["theme"] = {"name": "alpha", "locked": True}
    s["reels"]["location"]["enabled"] = False
    out = mp4.roll(s, mp4.REEL_NAMES, 1, registry=reg)
    assert out["state"]["reels"]["location"]["text"] == "" and "location" not in out["rolled"]
    assert h.calls[0]["include_environment"] is False and "env" not in out["prompt"]
    s2 = out["state"]; s2["reels"]["location"]["enabled"] = True
    assert mp4.roll(s2, ["location"], 2, registry=reg)["state"]["reels"]["location"]["text"] == "env 2"

def test_roll_frozen_prompt_skips_handlers():
    mp4 = _mp4()
    reg, h = _registry()
    s = mp4.default_state(); s["frozen_prompt"] = "fixed"
    out = mp4.roll(s, mp4.REEL_NAMES, 1, registry=reg)
    assert out["prompt"] == "fixed" and out["rolled"] == [] and h.calls == []

def test_roll_handler_exception_returns_error_prompt():
    mp4 = _mp4()
    reg, _ = _registry(fail=True)
    s = mp4.default_state(); s["theme"] = {"name": "alpha", "locked": True}
    s["reels"]["style"]["text"] = "old"
    out = mp4.roll(s, mp4.REEL_NAMES, 1, registry=reg)
    assert out["prompt"].startswith("Error: KeyError") and out["segments"][0]["reel"] == "error"
    assert out["state"]["reels"]["style"]["text"] == "old" and out["rolled"] == []

def test_roll_uses_the_shared_generation_lock():
    mp4 = _mp4()
    class RecordingLock:
        entries = 0
        def __enter__(self): RecordingLock.entries += 1
        def __exit__(self, *a): return False
    reg, _ = _registry()
    original, mp4.GENERATION_LOCK = mp4.GENERATION_LOCK, RecordingLock()
    try:
        mp4.roll(mp4.default_state(), mp4.REEL_NAMES, 1, registry=reg)
        assert RecordingLock.entries == 1
    finally:
        mp4.GENERATION_LOCK = original
```

- [ ] **Step 2 : vérifier l'échec**

Run: `python3 tests/run_all.py 2>&1 | grep "FAIL test_roll" | wc -l`
Expected: `9`

- [ ] **Step 3 : implémenter `new_seed`, `COMPONENT_KEYS`, `roll`**

- [ ] **Step 4 : vérifier**

Run: `python3 tests/run_all.py | tail -3`
Expected: `SUMMARY: 72/72 passed, 0 failed`

- [ ] **Step 5 : commit**

```bash
git add Core_Nodes/mega_prompt_v4.py tests/test_mega_prompt_v4.py
git commit -m "feat(megaprompt-v4): pure roll() with locked/pinned/disabled reels and frozen prompt

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 5 : classe du node et enregistrement

**Files:**
- Modify: `Core_Nodes/mega_prompt_v4.py`
- Modify: `__init__.py:11` (import après la ligne V3), `:88` (mapping après `IsulionMegaPromptV3`), `:102` (display après V3) — CRLF
- Modify: `tests/fixtures/expected_node_keys.json` (insérer `"IsulionMegaPromptV4",` après `"IsulionMegaPromptV3",`), `tests/fixtures/node_contracts_v2.json` (ajouter la clé en fin d'objet, après `IsulionSpaceInvaders`, même indentation 2 espaces, LF)
- Test: `tests/test_mega_prompt_v4.py`

**Interfaces:**
- Consumes: `roll`, `new_seed`, `parse_state`, `DEFAULT_STATE`.
- Produces: `class IsulionMegaPromptV4` : `TITLE = "🕹️ Mega Prompt V4"`, `INPUT_TYPES` (voir Contraintes globales), `RETURN_TYPES = ("STRING",)`, `RETURN_NAMES = ("prompt",)`, `FUNCTION = "generate"`, `CATEGORY = "Isulion/Core"`, `OUTPUT_NODE = True`, `@classmethod IS_CHANGED(cls, machine_state) -> float("nan")`, `generate(self, machine_state: str) -> dict` = `result = roll(machine_state, REEL_NAMES, new_seed())` (le `new_seed` est lu comme global du module) → `{"ui": {"draw": [result]}, "result": (result["prompt"],)}`.

- [ ] **Step 1 : écrire les tests**

```python
import math

def test_node_contract_and_registration():
    pkg = import_package()
    cls = pkg.NODE_CLASS_MAPPINGS["IsulionMegaPromptV4"]
    assert pkg.NODE_DISPLAY_NAME_MAPPINGS["IsulionMegaPromptV4"] == "🕹️ Isulion Mega Prompt V4"
    assert cls.INPUT_TYPES() == {"required": {"machine_state": ("STRING", {"default": '{"version": 1}'})}}
    assert (cls.RETURN_TYPES, cls.RETURN_NAMES, cls.CATEGORY, cls.OUTPUT_NODE) == (("STRING",), ("prompt",), "Isulion/Core", True)
    assert math.isnan(cls.IS_CHANGED('{"version": 1}'))

def test_node_generate_rolls_everything_and_reports_ui():
    mp4 = _mp4()
    original, mp4.new_seed = mp4.new_seed, lambda: 5
    try:
        node = mp4.IsulionMegaPromptV4()
        out = node.generate('{"version": 1}')
        draw = out["ui"]["draw"]
        assert len(draw) == 1 and draw[0]["seed"] == 5 and out["result"] == (draw[0]["prompt"],)
        assert draw[0]["prompt"] and draw[0]["state"]["theme"]["name"] in mp4.get_theme_registry().handlers
        assert node.generate("garbage")["result"] == out["result"]  # same seed, default state => same prompt
    finally:
        mp4.new_seed = original
```

- [ ] **Step 2 : vérifier l'échec**

Run: `python3 tests/run_all.py 2>&1 | grep "FAIL test_node_" | wc -l`
Expected: `2`

- [ ] **Step 3 : implémenter la classe, puis enregistrer**

`__init__.py` : ajouter `from .Core_Nodes.mega_prompt_v4 import IsulionMegaPromptV4` sous l'import V3, l'entrée de `NODE_CLASS_MAPPINGS` sous `"IsulionMegaPromptV3"`, l'entrée de `NODE_DISPLAY_NAME_MAPPINGS` sous celle de la V3. Faire l'édition avec l'outil Edit (qui conserve les `\r\n` existants) et écrire les nouvelles lignes avec `\r\n`. Mettre à jour les deux fixtures.

- [ ] **Step 4 : vérifier, y compris les fins de ligne**

Run: `python3 tests/run_all.py | tail -3 && test "$(grep -c $'\r' __init__.py)" = "$(wc -l < __init__.py)" && echo CRLF-OK && grep -c $'\r' tests/fixtures/node_contracts_v2.json`
Expected: `SUMMARY: 74/74 passed, 0 failed`, `CRLF-OK`, `0`

- [ ] **Step 5 : commit**

```bash
git add Core_Nodes/mega_prompt_v4.py __init__.py tests/fixtures/expected_node_keys.json tests/fixtures/node_contracts_v2.json tests/test_mega_prompt_v4.py
git commit -m "feat(megaprompt-v4): register IsulionMegaPromptV4 node (single prompt output)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 6 : routes HTTP

**Files:**
- Create: `Core_Nodes/mega_prompt_v4_routes.py`
- Modify: `__init__.py` (CRLF) : après l'import V4, `from .Core_Nodes import mega_prompt_v4_routes  # noqa: F401  (registers /isulion/megaprompt_v4/* when PromptServer exists)`
- Test: `tests/test_mega_prompt_v4.py`

**Interfaces:**
- Consumes: `list_themes`, `parse_state`, `roll`, `new_seed`, `REEL_NAMES`.
- Produces :
  - `ROUTE_PREFIX = "/isulion/megaprompt_v4"`
  - `themes_payload() -> list[dict]` = `list_themes()`.
  - `roll_payload(body) -> tuple[int, dict]` : `body` non-dict → `(400, {"error": "body must be a JSON object"})` ; `reels = body.get("reels", list(REEL_NAMES))` non-liste ou contenant autre chose que des noms de `REEL_NAMES` → `(400, {"error": "unknown reel"})` ; `seed = body.get("seed")` gardé seulement si `int` non-bool dans `[0, 2**32)`, sinon `new_seed()` ; `state = parse_state(body.get("state"))` (tout état invalide retombe sur le défaut, status 200) ; `(200, roll(state, reels, seed))`.
  - `register_routes(server_instance=None) -> bool` : `inst = server_instance` ou, à défaut, `PromptServer.instance` obtenu par `from server import PromptServer` dans un `try/except Exception` (→ `None`). Si `inst is None` → `False`. Sinon enregistre `inst.routes.get(f"{ROUTE_PREFIX}/themes")` → `async def themes(request)` qui renvoie `_json(themes_payload(), 200)` et `inst.routes.post(f"{ROUTE_PREFIX}/roll")` → `async def roll_route(request)` qui lit `body = await request.json()` dans un `try/except Exception → None`, puis `status, payload = await asyncio.to_thread(roll_payload, body)` et renvoie `_json(payload, status)`. Renvoie `True`.
  - `_json(payload, status)` : `web.json_response(payload, status=status)` si `aiohttp.web` est importable (import module-level dans `try/except ImportError`, `web = None` sinon), sinon `(status, payload)` (chemin des tests).
  - En bas du module : `ROUTES_REGISTERED = register_routes()`.

- [ ] **Step 1 : écrire les tests**

```python
import asyncio

def _routes():
    import_package()
    from isulion_pkg.Core_Nodes import mega_prompt_v4_routes as routes
    return routes

def test_themes_payload_lists_registry_sorted():
    routes, mp4 = _routes(), _mp4()
    assert routes.themes_payload() == mp4.list_themes()

def test_roll_payload_rejects_invalid_input_and_tolerates_bad_state():
    routes = _routes()
    assert routes.roll_payload(None)[0] == 400 and routes.roll_payload([1])[0] == 400
    assert routes.roll_payload({"reels": "theme"})[0] == 400
    assert routes.roll_payload({"reels": ["wheel"]})[0] == 400
    status, payload = routes.roll_payload({"state": "garbage", "reels": ["style"], "seed": True})
    assert status == 200 and 0 <= payload["seed"] < 2**32 and payload["prompt"]
    status, payload = routes.roll_payload({"state": {"version": 1}, "reels": [], "seed": 9})
    assert status == 200 and payload["seed"] == 9 and payload["rolled"] == []

def test_register_routes_without_server_is_a_noop():
    assert _routes().register_routes() is False

def test_register_routes_with_fake_server_registers_both_handlers():
    routes = _routes()
    registered = {}
    class Routes:
        def get(self, path): return lambda fn: registered.setdefault(("GET", path), fn)
        def post(self, path): return lambda fn: registered.setdefault(("POST", path), fn)
    assert routes.register_routes(types.SimpleNamespace(routes=Routes())) is True
    assert set(registered) == {("GET", "/isulion/megaprompt_v4/themes"), ("POST", "/isulion/megaprompt_v4/roll")}
    class Req:
        def __init__(self, body): self._b = body
        async def json(self): return self._b
    status, payload = asyncio.run(registered[("POST", "/isulion/megaprompt_v4/roll")](Req({"reels": [], "seed": 1})))
    assert status == 200 and payload["seed"] == 1
    status, _ = asyncio.run(registered[("POST", "/isulion/megaprompt_v4/roll")](Req("x")))
    assert status == 400
    status, themes = asyncio.run(registered[("GET", "/isulion/megaprompt_v4/themes")](Req(None)))
    assert status == 200 and themes == routes.themes_payload()
```

- [ ] **Step 2 : vérifier l'échec**

Run: `python3 tests/run_all.py 2>&1 | grep -c "mega_prompt_v4_routes"`
Expected: au moins `1` (`ModuleNotFoundError` / `ImportError`)

- [ ] **Step 3 : implémenter `mega_prompt_v4_routes.py` et l'import dans `__init__.py` (CRLF)**

- [ ] **Step 4 : vérifier**

Run: `python3 tests/run_all.py | tail -3 && test "$(grep -c $'\r' __init__.py)" = "$(wc -l < __init__.py)" && echo CRLF-OK`
Expected: `SUMMARY: 78/78 passed, 0 failed`, `CRLF-OK`

- [ ] **Step 5 : commit**

```bash
git add Core_Nodes/mega_prompt_v4_routes.py __init__.py tests/test_mega_prompt_v4.py
git commit -m "feat(megaprompt-v4): themes and roll HTTP routes (aiohttp optional, pure handlers)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 7 : harnais JS et module pur `mega_prompt_v4_core.js`

**Files:**
- Create: `tests/js/fake_dom.mjs`, `tests/js/comfy_stub.mjs`, `tests/js/load_extension.mjs`, `tests/js/test_mega_prompt_v4.mjs`
- Create: `web/mega_prompt_v4_core.js`
- Create: `tests/test_mega_prompt_v4_js.py` ; Modify: `tests/run_all.py` (ajouter `"test_mega_prompt_v4_js"` en fin de `MODULES`)

**Interfaces:**
- Produces (`web/mega_prompt_v4_core.js`, aucune dépendance, aucun accès au DOM) :
  - `export const REELS = ["theme", "subject", "location", "style", "effects"]`, `export const ROLL_REELS = REELS.slice(1)`
  - `export function readState(raw) -> state` : même contrat que `parse_state` Python (accepte string JSON ou objet ; tout défaut → état v1 par défaut).
  - `export function shortText(text, max = 22) -> string` : retire `(` `)`, condense les espaces, prend des mots entiers tant que la longueur ≤ `max` (au moins un mot ; un premier mot plus long que `max` est coupé à `max - 1` + `…`) ; `""` → `"—"`.
  - `export function pickLang(navLang, stored) -> "fr" | "en"` : `stored` vaut s'il est `"fr"` ou `"en"`, sinon `fr` si `String(navLang).toLowerCase().startsWith("fr")`, sinon `en`.
  - `export function historyRows(history, max = 5) -> items` : favoris (dans l'ordre) puis non-favoris, tronqué à `max`.
  - `export const TEXT = { en: {...}, fr: {...} }` : mêmes clés dans les deux langues : `marquee: "PROMPT JACKPOT"`, `reels: {theme, subject, location, style, effects}` (fr : THÈME/SUJET/LIEU/STYLE/EFFETS), `pull`, `complexity: {simple, detailed, complex}` (fr : SIMPLE/DÉTAILLÉ/COMPLEXE), `lora`, `promptTitle`, `copy`, `copied`, `edit`, `ok`, `cancel`, `frozenBadge`, `history`, `draw` (fr `"TIRAGE #"`), `seed` (fr `"GRAINE "`), `searchPlaceholder`, `editPlaceholder`, `emptyHint`, `error`, `help: {title, close, sections: [[title, body], ...]}` couvrant : rôle du node, levier et exécution, chaque bouton des rouleaux (🔒 ◀ ▶ 🔍 ✏️ 👁/🚫), complexité, LoRA, écran PROMPT (clic sur un segment, copier, éditer / prompt figé), derniers tirages et favoris.
- Produces (`tests/js/fake_dom.mjs`) : `export function installFakeDom({ language = "fr-FR" } = {}) -> { flushFrames(), runTimers(ms), pendingTimers(), observers, docListeners() }`. Installe sur `globalThis` : `document` (`createElement`, `head`, `body`, `hidden=false`, `activeElement`, `addEventListener`/`removeEventListener` comptés, `getElementById` par parcours de l'arbre), `window = globalThis`, `navigator = {language}`, `localStorage` (Map : `getItem`/`setItem`/`removeItem`), `ResizeObserver` et `IntersectionObserver` (instances collectées dans `observers`, `observe`/`disconnect` posent `disconnected`), `requestAnimationFrame`/`cancelAnimationFrame` (file vidée par `flushFrames`), `setTimeout`/`clearTimeout`/`setInterval`/`clearInterval` virtuels (`runTimers(ms)` avance une horloge et exécute les échéances dans l'ordre ; `pendingTimers()` compte ce qui reste), `performance.now`, classes `Event`, `WheelEvent`, `KeyboardEvent` minimales. `FakeElement` : `tagName`, `children`, `parentNode`, `style = {}`, `classList` (`add`/`remove`/`toggle`/`contains`), `dataset`, `attributes` via `setAttribute`/`getAttribute`, `id`, `className`, `title`, `value`, `placeholder`, `tabIndex`, `hidden`, `disabled`, `textContent` (get = concaténation, set = remplace les enfants par un texte), `appendChild`/`append`/`removeChild`/`replaceChildren`/`remove`/`contains`, `addEventListener`/`removeEventListener`/`dispatchEvent` (fixe `target`, appelle les écouteurs du type puis remonte aux parents sauf `stopPropagation`), `focus`/`blur` (met `document.activeElement`), `select`, `scrollIntoView`, `getBoundingClientRect` → zéros, `offsetWidth = 0`.
- Produces (`tests/js/comfy_stub.mjs`) : `export const app = { extensions: [], registerExtension(ext) { app.extensions.push(ext) }, canvas: { canvas: { dispatchEvent() {} } }, graph: { getNodeById() { return null } } }` ; `export const api = { calls: [], responders: {}, async fetchApi(route, opts = {}) { ... } }` qui enregistre `{route, opts, body: opts.body ? JSON.parse(opts.body) : null}` dans `calls`, prend `responders[route]` (valeur, fonction ou promesse), renvoie `{ ok: true, status: 200, json: async () => body }` (ou `ok:false, status` si le responder renvoie `{ __status: n, ... }`).
- Produces (`tests/js/load_extension.mjs`) : `export async function loadExtension(name = "mega_prompt_v4") -> { app, api }` : lit `web/<name>.js`, remplace `"../../scripts/app.js"` et `"../../scripts/api.js"` par l'URL `file://` de `comfy_stub.mjs` et `"./mega_prompt_v4_core.js"` par l'URL `file://` absolue du vrai fichier, puis `await import("data:text/javascript;charset=utf-8," + encodeURIComponent(src))`.
- Produces (`tests/js/test_mega_prompt_v4.mjs`) : mini-runner `test(name, fn)` ; `await` séquentiel ; affiche `PASS`/`FAIL name` + pile ; `process.exitCode = failures ? 1 : 0` ; helper `makeNode()` qui renvoie un objet `{ widgets: [{ name: "machine_state", value: '{"version": 1}' }], size: [300, 200], properties: {}, graph: { changes: 0, change() { this.changes++ } }, setSize(s) { this.size = s }, setDirtyCanvas() {}, addDOMWidget(name, type, el, opts) { this.dom = { name, type, el, opts }; return this.dom } }` sur lequel on applique les méthodes du prototype patché (`nodeType = function () {}` ; `ext.beforeRegisterNodeDef(nodeType, { name: "IsulionMegaPromptV4" })` ; `Object.setPrototypeOf(node, nodeType.prototype)`).
- Produces (`tests/test_mega_prompt_v4_js.py`) : `test_js_extension_syntax_and_harness()` : si `shutil.which("node")` est `None`, affiche `[skip] node not installed` et retourne ; sinon `subprocess.run([node, "--check", f], check=True)` pour `web/mega_prompt_v4.js` et `web/mega_prompt_v4_core.js`, puis `subprocess.run([node, "tests/js/test_mega_prompt_v4.mjs"], check=True, timeout=120, cwd=ROOT)`.

- [ ] **Step 1 : écrire les tests du module pur dans `tests/js/test_mega_prompt_v4.mjs`**

```js
import assert from "node:assert/strict";
import { REELS, readState, shortText, pickLang, historyRows, TEXT } from "../../web/mega_prompt_v4_core.js";

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
  assert.equal(REELS.length, 5);
});
```

- [ ] **Step 2 : vérifier l'échec**

Run: `node tests/js/test_mega_prompt_v4.mjs; echo "exit=$?"`
Expected: erreur `Cannot find module .../web/mega_prompt_v4_core.js`, `exit=1`

- [ ] **Step 3 : implémenter `web/mega_prompt_v4_core.js`, `tests/js/fake_dom.mjs`, `tests/js/comfy_stub.mjs`, `tests/js/load_extension.mjs`, `tests/test_mega_prompt_v4_js.py` et la ligne dans `run_all.py`**

Dans `test_mega_prompt_v4_js.py`, `node --check` de `web/mega_prompt_v4.js` ne doit pas échouer si le fichier n'existe pas encore à cette tâche : ne vérifier que les fichiers présents (`if path.exists()`).

- [ ] **Step 4 : vérifier**

Run: `node tests/js/test_mega_prompt_v4.mjs && python3 tests/run_all.py | tail -3`
Expected: 5 `PASS`, puis `SUMMARY: 79/79 passed, 0 failed`

- [ ] **Step 5 : commit**

```bash
git add web/mega_prompt_v4_core.js tests/js tests/test_mega_prompt_v4_js.py tests/run_all.py
git commit -m "test(megaprompt-v4): Node harness with fake DOM and pure core helpers

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 8 : la borne — extension, rouleaux, levier, thème, `onExecuted`, nettoyage

**Files:**
- Create: `web/mega_prompt_v4.js`
- Test: `tests/js/test_mega_prompt_v4.mjs`

**Interfaces:**
- Consumes: `app`, `api` ; `readState`, `shortText`, `REELS`, `ROLL_REELS`, `TEXT`, `pickLang`, `historyRows` (Tâche 7) ; routes de la Tâche 6 ; `RollResult`.
- Produces :
  - Extension `name: "Isulion.MegaPromptV4"`, filtre `nodeData.name === "IsulionMegaPromptV4"`. Hooks chaînés comme dans `web/space_invaders.js` : `onNodeCreated` (masque `machine_state` via `hideWidget`, crée `root`, `this.addDOMWidget("prompt_jackpot", "isulion-prompt-jackpot", root, { getMinHeight: () => 560, hideOnZoom: false, serialize: false })`, `setSize([max(w, 480), max(h, 640)])`, `this._jackpotRaf = requestAnimationFrame(...)` qui instancie `new PromptJackpot(this, dataWidget, root)` dans un `try/catch` → `this._jackpot`, `dom.onRemove = () => this._disposeJackpot()`), `onConfigure` (`this._jackpot?.load()`), `onExecuted(message)` (`this._jackpot?.onExecuted(message?.draw?.[0])`), `onRemoved` et `_disposeJackpot()` idempotent.
  - `injectStyles()` : une fois, `<style id="isu-mpv4-styles">` dans `document.head` (keyframes préfixés `isu-mpv4-`), palette et durées de la maquette (`neon` 3 s, `blink` 1.2 s, `roll` 6 s, `spin` 0.09 s, `bounce` 0.45 s, `pop` 0.4 s), règle `.isu-mpv4-paused, .isu-mpv4-paused * { animation-play-state: paused !important }`, classes `isu-mpv4-locked`, `isu-mpv4-off`, `isu-mpv4-custom`, `isu-mpv4-spin`, `isu-mpv4-land`, `isu-mpv4-pull`, segments `isu-mpv4-seg-subject|location|style|effects|complexity|lora|frozen|error`.
  - `el(tag, cls, text) -> HTMLElement` helper ; `class PromptJackpot` :
    - `constructor(node, dataWidget, root)` : `reqId = 0`, `timers = new Set()`, `typing = null`, `disposed = false`, `visible = true`, `lang = pickLang(navigator.language, lsGet("isu-mpv4-lang"))`, `themes = []` ; `build()` ; observers + `document.addEventListener("visibilitychange", this.onVisibility)` ; `root.addEventListener("pointerdown", stopPropagation)` ; `root.addEventListener("wheel", e => app.canvas?.canvas?.dispatchEvent(new WheelEvent(e.type, e)), { passive: true })` (les conteneurs défilants — liste de recherche, panneau d'aide, textarea — posent leur propre écouteur `wheel` avec `stopPropagation`) ; `load()` ; `loadThemes()`.
    - `build()` : crée tout le DOM de la maquette et garde les références dans `this.ui` : `marquee`, `helpBtn`, `crt`, `reels[name] = { box, name, face, icon, label, btns: { lock, prev, next, search, edit, toggle } }` (seulement les boutons que la spec donne au rouleau), `lever`, `cx[simple|detailed|complex]`, `lora` (input), `out`, `copyBtn`, `editBtn`, `frozenBadge`, `hist`, `draws`, `seed`, `search: { panel, input, list }` (Tâche 8), `editor` (Tâche 9), `help` (Tâche 11).
    - `load()` : `this.state = readState(dataWidget.value)` ; `this.view = node.properties.isu_mpv4 ??= { draws: 0, seed: null, history: [], last: null }` ; `render()` ; si `view.last` → `renderPrompt(view.last.segments, false)`.
    - `commit()` : écrit `JSON.stringify(this.state)` dans le widget (si différent) + `callback` + `graph?.change()` + `setDirtyCanvas(true, true)` ; `saveView()` : `node.properties.isu_mpv4 = this.view`.
    - `loadThemes()` : `themesPromise ??= api.fetchApi("/isulion/megaprompt_v4/themes").then(r => r.json())` (module-level, remis à `null` en cas d'erreur) → `this.themes` puis `renderReels()`.
    - `async roll(reels)` : `const id = ++this.reqId` ; `POST /isulion/megaprompt_v4/roll` avec `{ method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ state: this.state, reels }) }` ; ignore si `id !== this.reqId || this.disposed` ; `!r.ok` → `showError(payload.error)` ; sinon `applyResult(payload, { animate: payload.rolled.length > 0, record: payload.rolled.length > 0 })`.
    - `applyResult(payload, { animate, record })` : `this.state = readState(payload.state)` ; `commit()` ; `view.last = payload` ; `view.seed = payload.seed` ; si `record` : `view.draws += 1` et `pushHistory(payload)` (Tâche 10 ; jusque-là no-op) ; `saveView()` ; `renderFooter()` ; si `animate` : `spinReels(payload.rolled, () => { renderReels(); typePrompt(payload.segments) })`, sinon `renderReels(); renderPrompt(payload.segments, false)`.
    - `onExecuted(payload)` : si `!payload` retour ; `this.reqId++` (invalide toute réponse `roll` en vol) ; `applyResult(payload, { animate: true, record: true })`.
    - `spinReels(names, done)` : lever `isu-mpv4-pull` 320 ms ; pour chaque rouleau `i` : classe `spin`, timer `450 + 280 * i` → retire `spin`, pose `land`, le dernier appelle `done()` ; si `names` est vide → `done()` tout de suite. Timers via `this.setTimer(fn, ms)` qui les enregistre dans `this.timers` et les retire à l'exécution.
    - `renderReels()` : thème → `icon` + `label` depuis `this.themes` (ou `theme_entry` du dernier payload, sinon `"🎰"` / `"?"`) ; autres → icône fixe (`subject "👤"`, `location "🗺️"`, `style "🎨"`, `effects "✨"`) + `shortText(text)` ; classes `locked`/`off`/`custom` ; libellés des boutons `🔒`/`🔓`, `👁`/`🚫`.
    - `renderPrompt(segments, animate)` / `typePrompt(segments)` : `out.replaceChildren()` puis un `span.isu-mpv4-seg.isu-mpv4-seg-<reel>` par segment avec `textContent`, séparés par des nœuds texte `", "`, plus le curseur ; les segments `subject|location|style|effects` ont un `click` → `this.roll([reel])` ; `typePrompt` écrit d'abord le texte complet 3 caractères par tick (`setInterval` 14 ms stocké dans `this.typing`) puis remplace par les segments ; `frozenBadge.hidden = !state.frozen_prompt`.
    - Boutons : `lock` → bascule `locked`, `commit()`, `renderReels()` ; `toggle` → bascule `enabled`, `commit()`, `roll([])` ; `prev`/`next` → `setTheme(name)` du voisin dans `this.themes` (index −1 → 0) ; `setTheme(name)` : `theme = { name, locked: true }`, `commit()`, `roll(ROLL_REELS)` ; `search` → ouvre `search.panel`, filtre `label.toLowerCase().includes(q)` sur `input`, clic sur une ligne → `setTheme`, `Escape` ferme ; `lever` → si `state.frozen_prompt` : `state.frozen_prompt = ""` ; `roll(REELS)` ; `cx` → `state.complexity = v`, `commit()`, `roll([])` ; `lora` → sur `change` : `state.lora = value`, `commit()`, `roll([])` ; `copyBtn` → `navigator.clipboard?.writeText(view.last?.prompt ?? "")`, libellé `TEXT.copied` 1,2 s.
    - Les `input`/`textarea` posent `keydown` avec `stopPropagation()` (LiteGraph ne doit pas recevoir Delete/Backspace pendant la saisie).
    - `onVisibility()` / IntersectionObserver → `updatePaused()` : `root.classList.toggle("isu-mpv4-paused", !this.visible || document.hidden)`.
    - `dispose()` : idempotent (`disposed`), `reqId++`, `clearTimeout` de `timers`, `clearInterval(typing)`, `cancelAnimationFrame`, `disconnect()` des deux observers, retrait des écouteurs `document` (dont ceux de l'aide, Tâche 11), `root.replaceChildren()`.

- [ ] **Step 1 : écrire les tests (ajout au fichier `.mjs`)**

```js
import { installFakeDom } from "./fake_dom.mjs";
import { loadExtension } from "./load_extension.mjs";
import { makeNode } from "./test_mega_prompt_v4.mjs"; // helper défini dans ce même fichier (pas d'import réel)

const fake = installFakeDom();
const { app, api } = await loadExtension();
const ext = app.extensions.find((e) => e.name === "Isulion.MegaPromptV4");
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

test("registers extension and builds the cabinet once per node", async () => {
  assert.ok(ext); const node = await createNode();
  assert.ok(node._jackpot); assert.equal(node.dom.opts.serialize, false); assert.equal(node.dom.opts.hideOnZoom, false);
  assert.equal(node.widgets[0].hidden, true); assert.equal(node.widgets[0].type, "converted-widget");
  await createNode();
  assert.equal(document.head.children.filter((c) => c.id === "isu-mpv4-styles").length, 1);
});
test("lever posts a roll for all reels and applies the result", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload();
  node._jackpot.ui.lever.dispatchEvent(new Event("click")); await tick(); await tick();
  assert.deepEqual(lastRoll().body.reels, REELS); fake.runTimers(5000);
  assert.equal(JSON.parse(node.widgets[0].value).theme.name, "anime");
  assert.ok(node._jackpot.ui.out.textContent.includes("hero, forest")); assert.ok(node.graph.changes >= 1);
  assert.equal(node.properties.isu_mpv4.last.seed, 482913);
});
test("lock writes the state without rolling", async () => {
  const node = await createNode(); const before = api.calls.length;
  node._jackpot.ui.reels.subject.btns.lock.dispatchEvent(new Event("click"));
  assert.equal(JSON.parse(node.widgets[0].value).reels.subject.locked, true); assert.equal(api.calls.length, before);
});
test("next theme locks the theme and rerolls the other reels", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload();
  node._jackpot.state.theme.name = "anime";
  node._jackpot.ui.reels.theme.btns.next.dispatchEvent(new Event("click")); await tick();
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
  node._jackpot.ui.lever.dispatchEvent(new Event("click")); await tick();
  node.onExecuted({ draw: [payload({ prompt: "server wins", segments: [{ reel: "subject", text: "server wins" }] })] });
  resolve(payload({ prompt: "late", segments: [{ reel: "subject", text: "late" }] })); await tick(); await tick(); fake.runTimers(5000);
  assert.equal(node._jackpot.ui.out.textContent.replace(/\s+$/, ""), "server wins");
});
test("removing the node twice is safe and leaves nothing running", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload();
  node._jackpot.ui.lever.dispatchEvent(new Event("click")); await tick(); await tick();
  node.onRemoved(); node.dom.onRemove(); node._disposeJackpot();
  assert.equal(node._jackpot, null); assert.equal(fake.pendingTimers(), 0); assert.equal(fake.docListeners(), 0);
  assert.ok(fake.observers.every((o) => o.disconnected));
});
```

(Le `makeNode` est une fonction locale du fichier de test, pas un import : retirer la ligne d'import fictive.)

- [ ] **Step 2 : vérifier l'échec**

Run: `node tests/js/test_mega_prompt_v4.mjs; echo "exit=$?"`
Expected: `ENOENT ... web/mega_prompt_v4.js`, `exit=1`

- [ ] **Step 3 : implémenter `web/mega_prompt_v4.js`**

Les panneaux de recherche et d'édition et l'aide sont construits dans `build()` dès cette tâche (éléments cachés) ; leur comportement arrive aux Tâches 9 et 11.

- [ ] **Step 4 : vérifier**

Run: `node --check web/mega_prompt_v4.js && node tests/js/test_mega_prompt_v4.mjs && python3 tests/run_all.py | tail -3`
Expected: 12 `PASS`, `SUMMARY: 79/79 passed, 0 failed`

- [ ] **Step 5 : commit**

```bash
git add web/mega_prompt_v4.js tests/js/test_mega_prompt_v4.mjs
git commit -m "feat(megaprompt-v4): arcade cabinet DOM widget with reels, lever, theme and onExecuted sync

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 9 : saisie sur l'écran (✏️ Sujet/Lieu) et prompt figé (✏️ ÉDITER)

**Files:**
- Modify: `web/mega_prompt_v4.js`
- Test: `tests/js/test_mega_prompt_v4.mjs`

**Interfaces:**
- Consumes: `PromptJackpot` (Tâche 8), `state.reels.<r>.custom`, `state.frozen_prompt`.
- Produces :
  - `openInlineEdit(reel)` : montre `ui.editor.panel` (absolu sur le CRT, style arcade) avec `ui.editor.input` prérempli par `state.reels[reel].custom`, `ui.editor.clear` (✕), focus ; `Enter` → `state.reels[reel].custom = input.value.trim()`, `commit()`, fermeture, `roll([reel])` ; `Escape` ou clic hors champ → fermeture sans changement ; clic ✕ → `custom = ""`, `commit()`, fermeture, `roll([reel])`.
  - `openPromptEditor()` : montre `ui.editor.textarea` prérempli par `view.last?.prompt ?? ""` et `ui.editor.ok` ; `ok` → `state.frozen_prompt = textarea.value`, `commit()`, fermeture, `roll([])` ; `Escape`/`cancel` → fermeture. `frozenBadge` visible quand `state.frozen_prompt` est non vide (déjà prévu dans `renderPrompt`). Le levier quitte le mode figé (Tâche 8).

- [ ] **Step 1 : écrire les tests**

```js
test("inline edit pins a custom subject and rerolls that reel", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload();
  const j = node._jackpot; j.ui.reels.subject.btns.edit.dispatchEvent(new Event("click"));
  assert.equal(j.ui.editor.panel.hidden, false); j.ui.editor.input.value = "  my elf queen ";
  j.ui.editor.input.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter" })); await tick();
  assert.equal(lastRoll().body.state.reels.subject.custom, "my elf queen"); assert.deepEqual(lastRoll().body.reels, ["subject"]);
  assert.equal(j.ui.editor.panel.hidden, true);
});
test("escape cancels the inline edit", async () => {
  const node = await createNode(); const before = api.calls.length; const j = node._jackpot;
  j.ui.reels.location.btns.edit.dispatchEvent(new Event("click")); j.ui.editor.input.value = "x";
  j.ui.editor.input.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }));
  assert.equal(j.state.reels.location.custom, ""); assert.equal(api.calls.length, before); assert.equal(j.ui.editor.panel.hidden, true);
});
test("edit prompt freezes it and the lever unfreezes", async () => {
  const node = await createNode(); api.responders["/isulion/megaprompt_v4/roll"] = payload({ rolled: [], segments: [{ reel: "frozen", text: "fixed text" }], prompt: "fixed text" });
  const j = node._jackpot; j.ui.editBtn.dispatchEvent(new Event("click")); j.ui.editor.textarea.value = "fixed text";
  j.ui.editor.ok.dispatchEvent(new Event("click")); await tick();
  assert.equal(lastRoll().body.state.frozen_prompt, "fixed text"); assert.deepEqual(lastRoll().body.reels, []); await tick();
  assert.equal(j.ui.frozenBadge.hidden, false);
  j.ui.lever.dispatchEvent(new Event("click")); await tick();
  assert.equal(lastRoll().body.state.frozen_prompt, ""); assert.deepEqual(lastRoll().body.reels, REELS);
});
```

- [ ] **Step 2 : vérifier l'échec**

Run: `node tests/js/test_mega_prompt_v4.mjs 2>&1 | grep -c FAIL`
Expected: `3`

- [ ] **Step 3 : implémenter `openInlineEdit`, `openPromptEditor` et leurs écouteurs**

- [ ] **Step 4 : vérifier**

Run: `node --check web/mega_prompt_v4.js && node tests/js/test_mega_prompt_v4.mjs | tail -1 && python3 tests/run_all.py | tail -1`
Expected: aucun `FAIL`, `79/79`

- [ ] **Step 5 : commit**

```bash
git add web/mega_prompt_v4.js tests/js/test_mega_prompt_v4.mjs
git commit -m "feat(megaprompt-v4): on-screen custom text input and frozen prompt editor

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 10 : derniers tirages, favoris, pied de borne

**Files:**
- Modify: `web/mega_prompt_v4.js`
- Test: `tests/js/test_mega_prompt_v4.mjs`

**Interfaces:**
- Consumes: `historyRows` (Tâche 7), `applyResult` (Tâche 8), `view.history` (`{ payload, fav }`).
- Produces :
  - `pushHistory(payload)` : `view.history.unshift({ payload, fav: false })` ; garde au plus 5 favoris et 5 non-favoris (les non-favoris les plus anciens sortent) ; `renderHistory()`.
  - `renderHistory()` : titre `TEXT.history`, puis une ligne par `historyRows(view.history)` : `01…05`, `payload.prompt` (`textContent`, ellipsé par CSS `white-space: nowrap; overflow: hidden; text-overflow: ellipsis` — jamais de défilement horizontal), étoile `☆`/`★` ; clic sur l'étoile → bascule `fav`, `saveView()`, `renderHistory()` ; clic sur la ligne → `applyResult(item.payload, { animate: false, record: false })`.
  - `renderFooter()` : `draws.textContent = TEXT.draw + String(view.draws).padStart(3, "0")`, `seed.textContent = TEXT.seed + (view.seed ?? "—")`.

- [ ] **Step 1 : écrire les tests**

```js
test("history keeps five lines, favourites first, and reloads a line", async () => {
  const node = await createNode(); const j = node._jackpot;
  for (let n = 1; n <= 7; n++) { node.onExecuted({ draw: [payload({ prompt: `p${n}`, seed: n, segments: [{ reel: "subject", text: `p${n}` }] })] }); fake.runTimers(5000); }
  assert.equal(j.ui.hist.rows.length, 5); assert.equal(j.ui.hist.rows[0].text.textContent, "p7");
  j.ui.hist.rows[2].star.dispatchEvent(new Event("click"));                       // p5 becomes a favourite
  node.onExecuted({ draw: [payload({ prompt: "p8", seed: 8 })] }); fake.runTimers(5000);
  assert.equal(j.ui.hist.rows[0].text.textContent, "p5"); assert.equal(j.ui.hist.rows[0].star.textContent, "★");
  assert.equal(j.ui.hist.rows[1].text.textContent, "p8");
  j.ui.hist.rows[1].row.dispatchEvent(new Event("click"));
  assert.equal(node.properties.isu_mpv4.last.seed, 8); assert.equal(j.ui.draws.textContent, "TIRAGE #008");
  assert.equal(node.properties.isu_mpv4.history.length, 6);                      // 1 favourite + 5 recent
});
```

- [ ] **Step 2 : vérifier l'échec**

Run: `node tests/js/test_mega_prompt_v4.mjs 2>&1 | grep -c FAIL`
Expected: `1`

- [ ] **Step 3 : implémenter `pushHistory`, `renderHistory` (`ui.hist.rows = [{ row, text, star }]`), `renderFooter`**

- [ ] **Step 4 : vérifier**

Run: `node --check web/mega_prompt_v4.js && node tests/js/test_mega_prompt_v4.mjs | tail -1 && python3 tests/run_all.py | tail -1`
Expected: aucun `FAIL`, `79/79`

- [ ] **Step 5 : commit**

```bash
git add web/mega_prompt_v4.js tests/js/test_mega_prompt_v4.mjs
git commit -m "feat(megaprompt-v4): last draws list with favourites, draw counter and seed footer

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 11 : panneau d'aide « ? » EN / FR

**Files:**
- Modify: `web/mega_prompt_v4.js`
- Test: `tests/js/test_mega_prompt_v4.mjs`

**Interfaces:**
- Consumes: `TEXT`, `pickLang`, `this.lang`.
- Produces :
  - `ui.helpBtn` (rond, néon, « ? », en haut à droite à côté de l'enseigne) ; `ui.help = { panel, close, langEn, langFr, body }` ; `openHelp()` / `closeHelp()` / `toggleHelp()`.
  - `renderHelp()` : `body.replaceChildren()` puis pour chaque `[title, text]` de `TEXT[lang].help.sections` un `h4` + `p` en `textContent` ; panneau opaque par-dessus la borne, police non monospace, défilement vertical avec écouteur `wheel` qui `stopPropagation`.
  - `setLang(lang)` : `this.lang = lang` ; `lsSet("isu-mpv4-lang", lang)` (`lsGet`/`lsSet` enveloppent `localStorage` dans `try/catch`) ; `renderHelp()` et `renderLabels()` (tous les libellés `TEXT[lang]` de la borne : enseigne, noms de rouleaux, PULL, complexité, LoRA, PROMPT, COPIER/ÉDITER, titre de l'historique, pied).
  - Échap : écouteur `keydown` posé sur `document` en phase de capture à l'ouverture, retiré à la fermeture et dans `dispose()`.

- [ ] **Step 1 : écrire les tests**

```js
test("help panel opens in the browser language, switches to EN and remembers it", async () => {
  const node = await createNode(); const j = node._jackpot;
  assert.equal(j.lang, "fr"); assert.equal(j.ui.help.panel.hidden, true);
  j.ui.helpBtn.dispatchEvent(new Event("click")); assert.equal(j.ui.help.panel.hidden, false);
  assert.ok(j.ui.help.body.textContent.includes(TEXT.fr.help.sections[0][0]));
  j.ui.help.langEn.dispatchEvent(new Event("click"));
  assert.equal(localStorage.getItem("isu-mpv4-lang"), "en"); assert.ok(j.ui.help.body.textContent.includes(TEXT.en.help.sections[0][0]));
  assert.equal(j.ui.reels.theme.name.textContent, TEXT.en.reels.theme);
  document.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" })); assert.equal(j.ui.help.panel.hidden, true);
  j.ui.helpBtn.dispatchEvent(new Event("click")); j.ui.helpBtn.dispatchEvent(new Event("click")); assert.equal(j.ui.help.panel.hidden, true);
  const node2 = await createNode(); assert.equal(node2._jackpot.lang, "en");
  localStorage.removeItem("isu-mpv4-lang");
});
```

- [ ] **Step 2 : vérifier l'échec**

Run: `node tests/js/test_mega_prompt_v4.mjs 2>&1 | grep -c FAIL`
Expected: `1`

- [ ] **Step 3 : implémenter l'aide et `setLang`/`renderLabels`**

- [ ] **Step 4 : vérifier**

Run: `node --check web/mega_prompt_v4.js web/mega_prompt_v4_core.js && node tests/js/test_mega_prompt_v4.mjs | tail -1 && python3 tests/run_all.py | tail -1`
Expected: aucun `FAIL`, `79/79`

- [ ] **Step 5 : commit**

```bash
git add web/mega_prompt_v4.js tests/js/test_mega_prompt_v4.mjs
git commit -m "feat(megaprompt-v4): bilingual help panel with remembered language

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Tâche 12 : vérification de bout en bout

**Files:** aucun nouveau fichier (corrections éventuelles dans ceux des tâches précédentes).

- [ ] **Step 1 : suite complète et contrôles de forme**

Run: `python3 tests/run_all.py | tail -3 && node tests/js/test_mega_prompt_v4.mjs | grep -c PASS && test "$(grep -c $'\r' __init__.py)" = "$(wc -l < __init__.py)" && echo CRLF-OK && grep -c $'\r' tests/fixtures/node_contracts_v2.json tests/fixtures/expected_node_keys.json Core_Nodes/mega_prompt_v4.py Core_Nodes/mega_prompt_v4_routes.py web/mega_prompt_v4.js web/mega_prompt_v4_core.js`
Expected: `SUMMARY: 79/79 passed, 0 failed`, `17`, `CRLF-OK`, puis `0` pour chaque fichier listé.

- [ ] **Step 2 : contrôle des règles du skill sur le JS**

Run: `grep -nE "innerHTML|querySelector|window\.prompt|serialize: ?true|setInterval\(|setDirtyCanvas" web/mega_prompt_v4.js`
Expected: aucune ligne `innerHTML`, `querySelector`, `window.prompt`, `serialize: true` ; `setInterval(` apparaît une seule fois (frappe du prompt) ; `setDirtyCanvas` seulement dans `commit()`.

- [ ] **Step 3 : essai manuel dans ComfyUI (si disponible)**

Copier le dépôt dans `custom_nodes`, redémarrer, ajouter « 🕹️ Isulion Mega Prompt V4 » : la borne s'affiche, le levier tire sans lancer le workflow, Queue Prompt fait tourner les rouleaux et affiche exactement la sortie `prompt` (brancher un « Show Text » pour comparer), recharger la page restaure l'état et l'historique, le node s'exécute sans navigateur (`POST /prompt` en API) avec `machine_state = '{"version": 1}'`.

- [ ] **Step 4 : `git status` propre**

Run: `git status --short`
Expected: seulement `?? .superpowers/` (jamais ajouté).
