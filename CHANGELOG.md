# Changelog

## 6.2.0 — 2026-10-20

### New

- **🕹️ Isulion Mega Prompt V4 "Prompt Jackpot"**: an arcade slot machine drawn inside the node, with a single `prompt` output.
  - Five reels: Theme (◀ ▶ 🔍 across the 109 themes), Subject, Place, Style, Effects.
  - 🔒 lock per reel, ✏️ your own text pinned on Subject and Place, 👁/🚫 to switch Place, Style and Effects on or off.
  - PULL lever to preview draws without running the workflow; the machine also spins on every workflow run.
  - SIMPLE / DETAILED / COMPLEX complexity and a LoRA field.
  - Coloured PROMPT screen: click a piece to re-draw that reel, copy, or edit to freeze a hand-written prompt.
  - Last 5 draws with favourites, and a built-in "?" help in English and French.
  - Mega Prompt V3 stays available, unchanged.
- **👾 Isulion Space Invaders**: a game playable inside the node; outputs `high_score`, `last_score` and `summary`.
- The pack now declares a `WEB_DIRECTORY` (`web/`) for the frontend of its interactive nodes.
- New example workflow `Simple_Megaprompt_V4.workflow.json`.

### Changed

- Mega Prompt V3 seeding and generation share a lock with V4, so concurrent runs cannot mix their random draws.
- The Civitai example workflows no longer carry the value of the `api_key` widget removed in 6.1.0.
- README rewritten, with a French translation (`README.fr.md`).

## 6.1.0

### Breaking changes

- **Civitai Explorer / Civitai Trending no longer take an `api_key` widget.** Set the `CIVITAI_API_TOKEN` environment variable instead — this prevents API tokens from leaking into shared workflow files.
- **URL/image download nodes now refuse non-http(s) schemes and private/internal network addresses** (SSRF protection).
- **IsulionLoadImagesNode resolves directories strictly inside ComfyUI's input directory**; absolute paths outside it are rejected.
- **Selector nodes use an instance-seeded RNG**: the same seeds give the same results regardless of execution order.
- **Negative Prompt Generator pools are de-duplicated**: `strict` now yields 32–43 unique terms (previously 60–80 picks, many of them duplicates), so outputs for a given seed differ from v6.0.
- **🎲 Dynamic Random** may pick a different theme for a given seed than v6.0, because themes are now discovered automatically (alphabetical order).
