#!/usr/bin/env python3
"""
inject_assets.py — turn a token-placeholder storyboard template into a
self-contained HTML file by inlining assets, so it can be published as an
Artifact (CSP blocks external hosts) and opened offline.

The template is plain HTML that uses three kinds of tokens:

  {{ASSET:<filename>}}        -> a data: URI for that file in the assets dir.
                                 Works for .svg .webp .png .jpg .jpeg .gif.
                                 Use it in <img src> or CSS url('...').
  {{LOTTIE_LIB}}              -> the full lottie-web player source (inline).
                                 Put it inside a <script>...</script> once.
  {{LOTTIE_JSON:<filename>}}  -> the raw JSON text of a Lottie file, so the
                                 template can do:  var WAVE = {{LOTTIE_JSON:wave.json}};

Everything else (status bar, plan card, timeline, etc.) is just written
inline in the template as normal HTML — keep the injector dumb and generic so
it works for any screen set.

Usage:
  python inject_assets.py --template A_src.html --assets ./img/asset --out A.html
  # --lottie defaults to ../assets/lottie.min.js next to this script
"""
import argparse, base64, pathlib, re, sys

MIME = {".svg": "image/svg+xml", ".webp": "image/webp", ".png": "image/png",
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif"}

def data_uri(path: pathlib.Path) -> str:
    mime = MIME.get(path.suffix.lower())
    if not mime:
        raise SystemExit(f"[inject] unsupported asset type for data URI: {path.name}")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--assets", required=True, help="folder with exported svg/webp/lottie assets")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lottie", default=str(pathlib.Path(__file__).resolve().parent.parent / "assets" / "lottie.min.js"))
    args = ap.parse_args()

    assets = pathlib.Path(args.assets)
    html = pathlib.Path(args.template).read_text()

    def asset_repl(m):
        name = m.group(1).strip()
        p = assets / name
        if not p.exists():
            raise SystemExit(f"[inject] missing asset: {p}")
        return data_uri(p)
    html = re.sub(r"\{\{ASSET:([^}]+)\}\}", asset_repl, html)

    def json_repl(m):
        p = assets / m.group(1).strip()
        if not p.exists():
            raise SystemExit(f"[inject] missing lottie json: {p}")
        return p.read_text()  # raw JSON is valid JS
    html = re.sub(r"\{\{LOTTIE_JSON:([^}]+)\}\}", json_repl, html)

    if "{{LOTTIE_LIB}}" in html:
        lib = pathlib.Path(args.lottie)
        if not lib.exists():
            raise SystemExit(f"[inject] lottie lib not found: {lib}")
        html = html.replace("{{LOTTIE_LIB}}", lib.read_text())

    leftover = sorted(set(re.findall(r"\{\{[^}]+\}\}", html)))
    pathlib.Path(args.out).write_text(html)
    print(f"[inject] wrote {args.out} ({len(html):,} bytes)")
    if leftover:
        print(f"[inject] WARNING leftover tokens: {leftover}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
