# Skills for Designers

NativeCamp デザイナー向けの Claude Cowork スキル集です。
このリポジトリは **Cowork プラグインのマーケットプレイス** になっています。
GitHub に詳しくなくても、下の手順どおりに進めれば使えます。

---

## デザイナー向け：使い方

### ① 最初に1回だけ：マーケットプレイスを登録してインストール

**Cowork（デスクトップアプリ）の場合**

1. 右上の **Customize** →  **Plugins** を開く
2. 「Personal plugins」の **＋** ボタンを押す
3. **Add marketplace** を選ぶ
4. 次の文字列をそのまま貼り付ける：
   ```
   murakawa-nativecamp/Skills---for-Designers
   ```
5. **Add** を押す
6. 一覧に出てくる **nativecamp-design-skills** の **Install** を押す
7. **Done** を押す

これで完了です。会話で `/` を押すとスキルが使えます。

### ② 更新を取り込みたいとき

新しいバージョンが公開されたら、次のコマンドを実行すると最新になります：

```
/plugin marketplace update murakawa-nativecamp/Skills---for-Designers
```

（自動更新がオンの場合は、起動時に自動で最新化されます。）

---

## 収録スキル

| スキル名 | 説明 |
| --- | --- |
| nativecamp-figma-design-fix | NCxAIアプリ（ダークモード）で、参考画面に合わせて作成画面をDesign Systemで組み直す |

---

## メンテナー向け（編集する人）

- スキルの本体は `plugins/nativecamp-design-skills/skills/<スキル名>/SKILL.md` です。
- このフォルダがGitHubと自動同期されています。`SKILL.md` を編集して保存すれば、
  定期的に自動で GitHub に push され、バージョンも自動で上がります。
- 新しいスキルを追加するときは、`skills/` の下に `<スキル名>/SKILL.md` を作ります。
- 編集役は1人に集約するのが安全です（デザイナーはGitHubを直接触らない運用）。
