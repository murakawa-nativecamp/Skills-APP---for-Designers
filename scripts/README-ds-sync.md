# DS → スキル 自動同期（ds-sync）

Figma の **Design System - APP**（`DKl4vZ6OAtXYhuvMHbWkRZ`）で登録されている
変数・テキストスタイル・コンポーネントkeyを吸い出し、デザイナースキルの
「トークン早見表」を自動再生成して GitHub へ push する仕組み。

## 何が更新されるか
2つのスキルファイル内の `DS-AUTO:START … DS-AUTO:END` で囲まれたブロックだけ。
その外側（手書きのルール・コード例・CSSライブラリ）は一切触らない。

- `plugins/nativecamp-design-skills/skills/nativecamp-figma-design-fix/SKILL.md`
- `plugins/nativecamp-design-skills/skills/nativecamp-app-design-board/references/design-system.md`

## 制約（重要）
Figma の変数APIはこのプランでは REST から読めないため、**Figma デスクトップアプリで
DSファイルを開いた状態**でしか読み取れない。無人では動かない（＝要在席）。
DSファイルが開かれていない時は「確認できず。スキップ」で安全に終了する。

## 手動で実行する場合（Cowork で頼む）
1. Figma デスクトップで Design System - APP を開いておく。
2. Cowork で「DSスキルを更新して」と頼む。中では次が走る:
   - `scripts/ds_dump.js` の中身を Figma MCP `use_figma`（fileKey=`DKl4vZ6OAtXYhuvMHbWkRZ`）に渡して実行 → JSON取得
   - JSON を `scripts/ds_tokens.json` に保存（`meta.generatedAt` を現在時刻に）
   - `python3 scripts/ds_generate.py` で2ファイルのブロックを再生成
   - `bash scripts/sync.sh` で差分があれば版上げ＋push

## 自動実行
スケジュールタスク `sync-ds-tokens`（平日 09:30）。Figmaが開いていればリフレッシュ、
なければスキップ。詳細は `~/Claude/Scheduled/sync-ds-tokens/SKILL.md`。

## ファイル
- `ds_dump.js` … use_figma に渡す読み取り専用スクリプト（変数/スタイル/コンポーネントkey）
- `ds_generate.py` … ds_tokens.json → スキルの DS-AUTO ブロックを再生成（マーカー間だけ置換・冪等）
- `ds_tokens.json` … 最新スナップショット（差分が見えるよう commit 対象）

## 注意
- 別ファイルで変数を使う時は各 token の **key** を `importVariableByKeyAsync(key)` で解決する。
  VariableID の `…/xx:yy` 部分は作業ファイル固有なので、可搬な識別子は key のみ。
- アイコンのコンポーネントセットは別ライブラリ管理のため、この同期には含めていない。
