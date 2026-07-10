---
name: nativecamp-app-design-storyboard
description: >-
  Turn NativeCamp **mobile-app** designs (iOS / Android, Figma) into
  self-contained, production-faithful HTML "screen storyboard" artifacts, and
  package them into a zip for developers. Use this whenever the user wants to
  HTML-ify an app design, build a design/screen storyboard, reproduce app screens
  as code, create a Variant A / Variant B screen board, or "hand the design to
  developers as HTML/zip" — especially for the NativeCamp Japanese-app
  new-registration flow (NJ-98853), onboarding/registration screens, or the
  dark-mode NCxAI UI. Triggers even when the user just says "デザインをHTML化して",
  "ストーリーボード作って", "画面をコード化", "AとBのアーティファクト作って",
  "開発者に渡すzipにして", or points at a Figma node/URL and wants the screens
  rebuilt faithfully. SCOPE: app (mobile) screens only — PC / web (SP-web) uses a
  different design system and is out of scope for this skill. This is the
  design→code sibling of nativecamp-spec-artifact (which is for spec DOCUMENTS,
  not screens).
---

# NativeCamp design → HTML screen storyboard

Reproduce app screens **faithfully enough to ship** (the board is treated as the
production look): real Figma assets, exact DS tokens, laid out screen-by-screen
on a light "design tool" board, published as an Artifact, and zippable for devs.

This is design→code. For requirement/spec/measurement **documents**, use
`nativecamp-spec-artifact` instead.

## Scope: app (mobile) only
This skill currently covers **iOS / Android app screens only**. The DS tokens,
phone-frame component library, and asset conventions here assume the mobile
dark-mode NCxAI UI. **PC / web (SP-web) uses a different design system** and is
**out of scope** — don't reuse this skill's CSS/components for a PC/web board.
If a PC/web storyboard is ever needed, treat it as a separate skill/design system.

## References (read as needed)
- `references/design-system.md` — DS tokens + the full reusable phone-frame CSS component library + status-bar / Lottie mount snippets. **Read first** — paste the `<style>` block once into the board.
- `references/component-snippets.md` — ready-to-paste markup for every screen type (splash, value-prop/swipe, question, sign up, card+trial, trial-started, log in, tutor).
- `references/figma-workflow.md` — how to pull node ids / structure / assets from Figma, and the important MCP gotchas (Apple/Google icon export, WorldPay placeholder).
- `scripts/inject_assets.py` — inline assets into a token template (makes it self-contained + CSP-safe).
- `scripts/make_zip.py` — package final HTML(s) + assets + README into a zip.
- `assets/lottie.min.js` — bundled lottie-web player (inlined via `{{LOTTIE_LIB}}`).

## Workflow

### 1. Scope the screens
Confirm the variant/flow and list the screens. New-registration flow:
- **Variant A (with onboarding):** Splash → Strength ×3 → Questions ×3 → Sign up → Card → Trial started (+ Log in / Tutor).
- **Variant B (no onboarding):** Splash → Sign up → Card → Trial started (+ Log in / Tutor). B's Sign up carries the Log in / tutor links; B's Log in / Tutor use a flat dark bg (A uses the warm glow).

### 2. Pull from Figma (`references/figma-workflow.md`)
`get_metadata` for node ids → `get_design_context` for exact values → `get_screenshot` for visual truth. Reproduce structure/tokens in the CSS library — never ship the returned React/Tailwind.

### 3. Export assets → `img/asset/`
`download_assets` gives the **original fill sources** (before rounding). Save icons as `ic_*.svg`, images as `img_*.webp` (original size — round in CSS), character as Lottie JSON. Identify unlabeled fills with a PIL contact sheet. Mind the Apple/Google gotcha (use standard glyphs; LINE/Facebook export fine).

### 4. Build a token template `<name>_src.html`
Paste the DS `<style>` once, then assemble screens from `component-snippets.md`
inside `.rail` sections. Reference every asset as `{{ASSET:<file>}}`, mount the
character with `{{LOTTIE_LIB}}` + `{{LOTTIE_JSON:<file>}}`. Keep captions English
and overview-only. Structural notes that matter for fidelity:
- The board page has **no** `<!doctype>/<html>/<head>/<body>` — the Artifact tool wraps it. Start with `<title>` then `<style>`.
- Each `.phone` is a fixed 375px frame; content inside is fluid (no fixed inner widths except intrinsic logo/lottie sizes).
- Group hero→dots in `.swipe` for value-prop screens (that region is the swipe/pager target).
- Timeline connector must span **dot→dot only** (the CSS library already guarantees this — don't reintroduce a `bottom`-anchored line).

### 5. Inject → self-contained HTML
```bash
python scripts/inject_assets.py --template <name>_src.html --assets ./img/asset --out <name>.html
```
Fails loudly on missing assets and reports leftover `{{…}}` tokens (should be none).

### 6. Publish as an Artifact
Load the `artifact-design` skill first (per the Artifact tool). Publish `<name>.html`; to revise, edit the `_src` template, re-inject, and republish to the **same URL** (`url:` param) so the link stays stable. Keep the favicon stable across redeploys.

### 7. Review-and-fix loop (BEFORE zipping)
Visual corrections are expected on every design→HTML job. Treat publish→review→
fix as a loop and **do not zip until the user signs off**:
publish the Artifact → user eyeballs the URL → they give per-screen fixes →
edit the `_src` template → re-inject → republish to the **same URL** → repeat.
Because this environment usually can't render in a browser, the published URL is
the review surface — ask the user to confirm each round, and only proceed to the
zip when they say it's good.

### 8. Zip for developers (on request, after sign-off)
```bash
python scripts/make_zip.py --name NJ-XXXXX_storyboards \
  --html A.html:design_storyboard_A.html B.html:design_storyboard_B.html \
  --assets ./img/asset --out ./artifacts/NJ-XXXXX_storyboards_AB.zip
```
Generates a developer README automatically (self-contained HTML + source assets
+ notes). Uploading/sending the zip is the user's step — don't send externally
without being asked.

## Verify before handing off
This environment usually can't render in a browser (sandbox), so: confirm
`inject_assets.py` reports **no leftover tokens**, structural counts look right
(phones, `data:` URIs, `id="lottie"` containers, tags balanced), and tell the
user to eyeball the published URL — call out that **Lottie playback and exact
visual need their confirmation**, and offer per-screen fixes.

## Keeping specs in sync
If a design change also affects a requirement/measurement doc, update the JA **and**
EN versions and related tickets together (see the user's standing preference).
