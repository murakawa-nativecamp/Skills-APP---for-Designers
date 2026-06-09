#!/usr/bin/env bash
# 自動同期スクリプト（堅牢版）
# マスターフォルダ内には .git を置かず、毎回 /tmp で一時的に clone して push する。
# これにより、Mac→Linux マウント上での git ロック問題を回避する。
#
# 使い方: bash scripts/sync.sh
# 前提:  マスターフォルダ直下に .sync-config（GH_REPO / GH_TOKEN など）があること。
set -euo pipefail

MASTER="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# --- 設定読み込み ---
if [ ! -f "$MASTER/.sync-config" ]; then
  echo "ERROR: .sync-config が見つかりません ($MASTER)"; exit 1
fi
# shellcheck disable=SC1090
source "$MASTER/.sync-config"
: "${GH_REPO:?GH_REPO 未設定}"
: "${GH_TOKEN:?GH_TOKEN 未設定}"
GIT_USER_NAME="${GIT_USER_NAME:-NativeCamp Design}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-noreply@example.com}"

mask() { sed -E 's#github_pat_[A-Za-z0-9_]+#github_pat_***#g'; }

# --- 一時作業ディレクトリ（native FS）---
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# --- clone ---
git clone --quiet "https://${GH_TOKEN}@github.com/${GH_REPO}.git" "$WORK/repo" 2>&1 | mask
cd "$WORK/repo"
git config user.name "$GIT_USER_NAME"
git config user.email "$GIT_USER_EMAIL"

# --- マスターの中身を clone にミラー（.git や除外物を除く）---
find . -mindepth 1 -not -path './.git' -not -path './.git/*' -exec rm -rf {} + 2>/dev/null || true
tar -C "$MASTER" \
    --exclude='./.git' --exclude='./_git_broken' \
    --exclude='.DS_Store' --exclude='./.sync-config' \
    -cf - . | tar -xf -

git add -A
if git diff --cached --quiet; then
  echo "変更なし。スキップしました。"
  exit 0
fi

# --- plugins/ に変更があればバージョンを patch +1 し、マスターにも書き戻す ---
if ! git diff --cached --quiet -- plugins; then
  python3 - "$WORK/repo" "$MASTER" <<'PY'
import json, sys, glob, os
clone, master = sys.argv[1], sys.argv[2]

def bump(v):
    p = (v or "0.0.0").split(".")
    while len(p) < 3: p.append("0")
    try: p[2] = str(int(p[2]) + 1)
    except ValueError: p[2] = "1"
    return ".".join(p[:3])

new = {}
for pj in glob.glob(os.path.join(clone, "plugins", "*", ".claude-plugin", "plugin.json")):
    d = json.load(open(pj, encoding="utf-8"))
    d["version"] = bump(d.get("version", "0.0.0"))
    new[d["name"]] = d["version"]
    json.dump(d, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=2); open(pj, "a").write("\n")
    rel = os.path.relpath(pj, clone)
    mpj = os.path.join(master, rel)
    if os.path.exists(mpj):
        json.dump(d, open(mpj, "w", encoding="utf-8"), ensure_ascii=False, indent=2); open(mpj, "a").write("\n")

mp = os.path.join(clone, ".claude-plugin", "marketplace.json")
if os.path.exists(mp):
    m = json.load(open(mp, encoding="utf-8"))
    for p in m.get("plugins", []):
        if p.get("name") in new: p["version"] = new[p["name"]]
    json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2); open(mp, "a").write("\n")
    mmp = os.path.join(master, ".claude-plugin", "marketplace.json")
    if os.path.exists(mmp):
        json.dump(m, open(mmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2); open(mmp, "a").write("\n")
print("bumped:", new)
PY
  git add -A
fi

git commit -q -m "sync: update skills ($(date '+%Y-%m-%d %H:%M'))"
git push --quiet origin HEAD:main 2>&1 | mask
echo "push 完了しました。"
