# Pulling designs & assets from Figma

File key for the new-registration flow: `cVNEiNf9y2Ga3uORjJpMRW`
Known group nodes: **A = 312:5360**, **B = 312:5361** (verify per task).

## Find the screen node ids
`get_metadata(nodeId=<group>)` returns the frame tree (names + ids + x/y/w/h).
The x/y/w/h are in the same 1:1 space as a 375-wide screenshot, so they double
as exact layout coordinates. If the output is too large, grep the saved tool
result for the screen names (e.g. `01_Splash`, `02_SignUp`, `03_TrialAndCard_*`,
`04_TrialStarted`, `G_01b_EmailLogIn_Default`, `G_01c_TutorLogIn_Default`).

## Get exact structure / tokens
`get_design_context(fileKey, nodeId, excludeScreenshot=true)` returns reference
code with the real values (spacing, font sizes/weights, colors, radii) and a
JSON of asset download URLs. Read the values, adapt to the CSS library — do NOT
ship the returned React/Tailwind.

`get_screenshot(nodeId)` — quick visual truth for copy and layout.

## Export assets — `download_assets(fileKey, nodeId)`
Returns an exported render **plus the original source images** (the fills,
BEFORE any rounded-corner crop) with a `format` field. Download the raw URLs
promptly (short-lived) and convert:
- **Icons → SVG** (curl the svg asset url; keep as `ic_*.svg`).
- **Images → WEBP** at the original size (PIL: `Image.open(png).save(x,"WEBP",quality=88,method=6)`). Name `img_*.webp`. Round corners in CSS, not in the asset.
- **Character → Lottie JSON** (usually already in the repo, e.g. `wave_animation.json`, `wave_blink_animation.json`).
Put everything in an `img/asset/` folder in the working project.

Identify which raw image is which by building a quick contact sheet (PIL
thumbnails) and viewing it — the fills come back unlabeled.

## Figma-MCP gotchas (important)
- **Apple / Google social-button icons export as the placeholder `navigation/home` icon.** The real glyph is an instance override the MCP can't resolve, so every export of those slots is byte-identical to the home icon. Use a correct standard Apple silhouette (white for sign-in, black for Apple Pay) and a standard multicolor Google "G". **LINE and Facebook DO export correctly** (`sns/line-circle`, `sns/facebook-color`).
- SVG icons use `fill="var(--fill-0, <color>)"` — they carry their intended color; you can recolor by setting `--fill-0` on a wrapper, or by string-replacing the color for a variant (e.g. white→#000 for the black Apple Pay logo).
- The Apple Pay button in Figma uses the SF `` glyph as text; the "Select Card" area is a WorldPay hosted-form screenshot — don't ship it, use the `.wp-ph` placeholder.
- `get_metadata` on a whole group can exceed the token limit — it gets saved to a file; grep it instead of reading whole.

## Localhost vs remote asset URLs
Two Figma MCP servers may be connected: one returns `http://localhost:3845/assets/*`, the other `https://www.figma.com/api/mcp/asset/*`. Both are curl-able locally while the Figma desktop app / session is live. `download_assets` (remote) is the most reliable for original fills.
