#!/usr/bin/env bash
# 自動同期スクリプト：plugins/ 配下に変更があれば、バージョンを patch で上げて commit & push する。
# .git/config にトークン付きリモートが設定済みであることが前提。
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

# 念のため最新化（push 競合を避ける）
git pull --rebase --autostash origin main 2>/dev/null || true

# plugins/ 配下の変更だけを対象に判定
if git diff --quiet -- plugins && git diff --cached --quiet -- plugins; then
  # 追跡外の新規ファイルもチェック
  if [ -z "$(git ls-files --others --exclude-standard -- plugins)" ]; then
    echo "no changes in plugins/, skip"
    exit 0
  fi
fi

# patch バージョンを +1 する（plugin.json と marketplace.json の両方）
python3 - "$REPO_DIR" <<'PY'
import json, sys, glob, os
root = sys.argv[1]

def bump(v):
    parts = (v or "0.0.0").split(".")
    while len(parts) < 3:
        parts.append("0")
    try:
        parts[2] = str(int(parts[2]) + 1)
    except ValueError:
        parts[2] = "1"
    return ".".join(parts[:3])

# plugin.json をすべて更新
new_versions = {}
for pj in glob.glob(os.path.join(root, "plugins", "*", ".claude-plugin", "plugin.json")):
    d = json.load(open(pj, encoding="utf-8"))
    d["version"] = bump(d.get("version", "0.0.0"))
    new_versions[d["name"]] = d["version"]
    json.dump(d, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(pj, "a", encoding="utf-8").write("\n")

# marketplace.json のエントリも合わせる
mp = os.path.join(root, ".claude-plugin", "marketplace.json")
m = json.load(open(mp, encoding="utf-8"))
for p in m.get("plugins", []):
    if p.get("name") in new_versions:
        p["version"] = new_versions[p["name"]]
json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(mp, "a", encoding="utf-8").write("\n")
print("bumped:", new_versions)
PY

git add -A
git commit -m "chore: sync skills ($(date +%Y-%m-%d\ %H:%M))" || { echo "nothing to commit"; exit 0; }
git push origin main
echo "pushed"
