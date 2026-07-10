#!/usr/bin/env python3
"""
make_zip.py — package finished storyboard HTML(s) + source assets + a README
into a single zip to hand to developers.

Usage:
  python make_zip.py \
    --name NJ-98853_storyboards \
    --html A.html:design_storyboard_A.html B.html:design_storyboard_B.html \
    --assets ./img/asset \
    --out ./artifacts/NJ-98853_storyboards_AB.zip \
    [--readme ./README.txt]      # if omitted, a sensible README is generated

Each --html entry is  <source-path>[:<name-inside-zip>].  If no name is given,
the source filename is used.  The zip contains:
  <name>/<html files>
  <name>/assets/<all files from --assets>
  <name>/README.txt
"""
import argparse, pathlib, shutil, tempfile, zipfile, os

DEFAULT_README = """{name}
{underline}

Contents
--------
{html_lines}
- assets/     Source assets (icons=SVG, images=WEBP original fills before the
              rounded-corner crop, character animation=Lottie JSON).
- README.txt  This file.

How to view
-----------
Open any .html file in a modern browser. The files are fully self-contained
(all images, icons and Lottie animations are embedded) so no server or network
is required. The phone frames are a fixed device width; the content inside is
fluid and follows the frame width.

Assets
------
Images are the ORIGINAL fill sources (before the rounded-corner crop) — apply
the corner radius in code. Icons are SVG; the character is a Lottie JSON.

Notes
-----
- Apple / Google logos use standard brand glyphs for their sign-in / pay
  buttons. LINE / Facebook (if present) are the real exported icons.
- The card "Select Card" area is a WorldPay hosted form (rendered by the
  WorldPay SDK) — shown as a placeholder.
- Design system: dark theme + orange (brand #f1890e; gradient #FF6B35 -> #EEB633);
  font Noto Sans JP.
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="top folder name inside the zip")
    ap.add_argument("--html", nargs="+", required=True, help="src.html[:name-in-zip] ...")
    ap.add_argument("--assets", help="folder of source assets to include (optional)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--readme", help="path to a README.txt (optional; generated if omitted)")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp) / args.name
        root.mkdir(parents=True)
        html_names = []
        for spec in args.html:
            src, _, dest = spec.partition(":")
            dest = dest or pathlib.Path(src).name
            shutil.copy(src, root / dest)
            html_names.append(dest)
        if args.assets:
            shutil.copytree(args.assets, root / "assets")
        if args.readme:
            shutil.copy(args.readme, root / "README.txt")
        else:
            html_lines = "\n".join(f"- {n}" for n in html_names)
            (root / "README.txt").write_text(DEFAULT_README.format(
                name=args.name, underline="=" * len(args.name), html_lines=html_lines))

        out = pathlib.Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(root.rglob("*")):
                z.write(f, f.relative_to(pathlib.Path(tmp)))
        print(f"[zip] wrote {out} ({out.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()
