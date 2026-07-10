#!/usr/bin/env python3
"""ds_generate.py — rebuild the DS-AUTO token blocks in the designer skills
from scripts/ds_tokens.json (produced by ds_dump.js via the Figma use_figma tool).

Only the content between the DS-AUTO:START / DS-AUTO:END markers is replaced.
Everything else in each skill file is left untouched. If the markers are not
present yet, the block is inserted right after a known anchor heading.

Usage:  python3 scripts/ds_generate.py
Exit:   0 = wrote / no-op, 1 = error (missing json / anchor)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOKENS = os.path.join(HERE, "ds_tokens.json")

FIX_SKILL = os.path.join(
    ROOT, "plugins", "nativecamp-design-skills", "skills",
    "nativecamp-figma-design-fix", "SKILL.md")
DS_DOC = os.path.join(
    ROOT, "plugins", "nativecamp-design-skills", "skills",
    "nativecamp-app-design-board", "references", "design-system.md")

START = "<!-- DS-AUTO:START — 自動生成 (scripts/ds_generate.py) / 手動編集しないでください -->"
END = "<!-- DS-AUTO:END -->"


def num(v):
    """Render a JSON number without a trailing .0 for whole numbers."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def color_rows(data, modes_wanted):
    sem = data["collections"]["Semantic"]
    modes = [m for m in modes_wanted if m in sem["modes"]]
    header = "| name | " + " | ".join(modes) + " | key |"
    sep = "|" + "---|" * (len(modes) + 2)
    lines = [header, sep]
    for v in sem["vars"]:
        cells = [v["name"]] + [str(v["val"].get(m, "")) for m in modes] + ["`%s`" % v["key"]]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def scale_rows(data, coll, unit="px"):
    c = data["collections"][coll]
    lines = ["| name | %s | key |" % unit, "|---|---|---|"]
    for v in c["vars"]:
        lines.append("| %s | %s | `%s` |" % (v["name"], num(v["val"]["Value"]), v["key"]))
    return "\n".join(lines)


def textstyle_rows(data):
    lines = ["| name | size | weight | line-height | key |", "|---|---|---|---|---|"]
    for s in data["textStyles"]:
        lines.append("| %s | %s | %s | %s | `%s` |" % (
            s["name"], num(s["size"]), s["weight"], s["lh"], s["key"]))
    return "\n".join(lines)


def component_rows(data):
    lines = ["| name | type | props | key |", "|---|---|---|---|"]
    for c in data.get("components", []):
        props = ", ".join(c.get("props", []))
        lines.append("| %s | %s | %s | `%s` |" % (c["name"], c["type"], props, c["key"]))
    return "\n".join(lines)


def block_for_fix_skill(data):
    ts = data["meta"].get("generatedAt", "AUTO")
    return "\n".join([
        START,
        "### 🔄 DS 自動同期トークン（自動生成ブロック・手動編集禁止）",
        "> 出典: Design System - APP (`%s`) ／ 生成日時: %s" % (data["meta"]["sourceFileKey"], ts),
        "> **別ファイルで使う時は各行の `key` を `importVariableByKeyAsync(key)` で解決する。**",
        "> VariableID は作業ファイル固有のローカルIDなので、可搬な識別子は key のみ。値/名前/keyはDS更新のたびにここへ再生成される。",
        "",
        "#### 色 (Semantic / Dark・Light)",
        color_rows(data, ["Dark", "Light"]),
        "",
        "#### Spacing (padding・gap は必ずこれにバインド)",
        scale_rows(data, "Spacing"),
        "",
        "#### Radius (cornerRadius)",
        scale_rows(data, "Radius"),
        "",
        "#### BorderWidth (strokeWeight)",
        scale_rows(data, "BorderWidth"),
        "",
        "#### Layout (wrapper padding / max-width)",
        scale_rows(data, "Layout"),
        "",
        "#### テキストスタイル (`setTextStyleIdAsync` は key を importByKey で解決)",
        textstyle_rows(data),
        "",
        "#### コンポーネント (component_set key)",
        component_rows(data),
        END,
    ])


def block_for_ds_doc(data):
    ts = data["meta"].get("generatedAt", "AUTO")
    return "\n".join([
        START,
        "## 🔄 DS auto-synced tokens (generated — do not edit by hand)",
        "> Source: Design System - APP (`%s`) / generated: %s" % (data["meta"]["sourceFileKey"], ts),
        "> Regenerated on every DS update by `scripts/ds_generate.py`. Values below are the source of truth.",
        "",
        "### Color (Dark / Light)",
        color_rows(data, ["Dark", "Light"]),
        "",
        "### Type — text styles",
        textstyle_rows(data),
        "",
        "### Spacing",
        scale_rows(data, "Spacing"),
        "",
        "### Radius",
        scale_rows(data, "Radius"),
        "",
        "### BorderWidth",
        scale_rows(data, "BorderWidth"),
        END,
    ])


def apply_block(path, block, anchor_regex):
    """Replace the DS-AUTO block in `path`, or insert it after the anchor line."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    if START in text and END in text:
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
        new_text = pattern.sub(lambda _m: block, text)
    else:
        m = re.search(anchor_regex, text, re.MULTILINE)
        if not m:
            raise SystemExit("ERROR: anchor not found in %s" % path)
        insert_at = m.end()
        new_text = text[:insert_at] + "\n\n" + block + "\n" + text[insert_at:]

    if new_text == text:
        print("no change: %s" % os.path.relpath(path, ROOT))
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("updated: %s" % os.path.relpath(path, ROOT))
    return True


def main():
    if not os.path.exists(TOKENS):
        raise SystemExit("ERROR: %s not found. Run ds_dump.js via use_figma first." % TOKENS)
    with open(TOKENS, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = False
    # figma-design-fix: insert after the "## DS トークン早見表" heading
    changed |= apply_block(FIX_SKILL, block_for_fix_skill(data),
                           r"^## DS トークン早見表.*$")
    # design-system.md: insert after the intro sentence mentioning Figma variables
    changed |= apply_block(DS_DOC, block_for_ds_doc(data),
                           r"^Reproduce screens faithfully with these tokens.*$")

    print("done." if changed else "done (no changes).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
