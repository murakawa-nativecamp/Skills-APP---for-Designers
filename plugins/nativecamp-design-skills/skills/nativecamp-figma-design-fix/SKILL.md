---
name: nativecamp-figma-design-fix
description: >
  NativeCamp の NCxAI アプリ（ダークモード専用）で Figma の画面を修正・作成するときに使う。
  「参考(reference)に合わせて作成画面(target)を直して」「Figmaを編集して」「DSに合わせて」
  「退会フローのこの画面を作って」など、Figma の特定ノードを編集する依頼で発動する。
  Figma MCP(use_figma) で DS コンポーネント/変数を使い、テキストは参考と同じに、
  レイアウトは Design System できれいに整える。design-to-figma / figma編集 / UI修正 が対象。
---
# NativeCamp Figma デザイン修正スキル
## 目的
「参考画面(reference)」を見ながら「作成画面(target frame)」の中身を、**現行 Design System(DS) のダークモード**で組み直す。
参考は旧コンポーネント/フラット構造のことが多い。**ガワ（DSヘッダー・main>wrapper-M>section 構造・DSボタン）は活かし、中身だけ作り込む**。
## 大原則
1. **テキスト内容は参考と完全に同じ**にする（文言・改行位置）。
2. **レイアウトは参考に縛られすぎない**。DS でクリーンに整える。
3. **色・テキストは必ず DS 変数 / テキストスタイルにバインド**する（生のHEX禁止）。
4. **余白(padding/gap)・角丸(radius)・線幅(strokeWeight)も必ず DS 変数（"Design System - APP" の Spacing / Radius / BorderWidth コレクション）にバインド**する。**生の数値直書きは禁止**。値が合わない時は最も近いトークンを選ぶ（任意の px を作らない）。**バインドできる箇所は全てバインド**：fills/strokes の色、paddingLeft/Right/Top/Bottom、itemSpacing、4隅 radius、strokeWeight。
5. **アイコンは Icon コンポーネントのインスタンス**で（直置きグリフ禁止）。
6. **タブバー(tab_navigation)は参考にある画面だけ残す**。無い画面は削除。
7. 確認は **構造データ（componentProperties / characters / boundVariables 等）で行う**。スクショは遅延・キャッシュがある。
## 入力
- 参考ノードURL（例 `?node-id=13354-10148`）
- 作成ノードURL（例 `?node-id=13354-11890`）
- fileKey はURLから抽出（`/design/<fileKey>/...`）。本プロジェクト作業ファイル: `R444smr7K5Btu854AGNibv`
## 既存デザイン資産の参照 ※重要
- これまで作成したデザインは **「App Master File for student」** に蓄積されている。
- **似た画面・要素・パターンを作るときは、まずこのファイルを参照**し、既存の構成・レイヤー命名・DSコンポーネントの使い方・余白の取り方を踏襲する（毎回ゼロから作らない／既存の作り方に合わせる）。
- ファイル: `https://www.figma.com/design/HKEeQO4ltPu3moj0U0FCwg/App-Master-File-for-student?node-id=1-491`
- fileKey: `HKEeQO4ltPu3moj0U0FCwg`（参照起点ノード: `1-491`）
- 参照手順: `get_metadata` / `get_screenshot` で近い既存画面を探し、その section/block 構成・使用コンポーネント・`boundVariables` の付け方を真似てから新規画面に適用する。新しい依頼を受けたら、着手前にまずここで類似デザインの有無を確認する。
## ワークフロー
1. **参考を読む**：`get_screenshot`（参考は静的なので正確）でテキスト/構成を把握。深い構造の読み取りはタイムアウトしやすいので **直下の子だけ・depth≤2** に。
2. **作成画面のガワを確認**：`header` / `main` > `wrapper-M` > `section_◯` / `tab_navigation` の構成を読む。**main の padding と wrapper-M の itemSpacing がどの DS 変数にバインドされているか** を `boundVariables` で確認してから踏襲する。
3. **ヘッダー**：`text_page_title` を参考タイトルに。右アイコン `slot_header_right` は基本 `visible=false`。
4. **本文を組む**：見出し→本文→画像/カード→入力等を section/block で構成。色・文字・余白・角丸・線幅を全てDS変数にバインド。
5. **ボタン**：主CTA=Primary(オレンジ)、副action=Secondary(白枠)。下部に配置。**単体なら囲まずそのまま置く**（後述「ボタンの置き方」）。
6. **タブ**：参考に無ければ `tab_navigation` を remove。あれば残し、main の `paddingBottom≈95〜120`（タブは絶対配置で浮くため）。
7. **レイアウト方式**を選ぶ（下記）。
8. **検証**：構造で確認（characters / fills.boundVariables / padding・strokeWeight の boundVariables）→ 可能ならスクショ（古い表示が出たらキャッシュ。少し待って再取得）。
## 余白(padding/gap)の付け方 ※重要・最頻出ミス
- **大外の余白は必ず `main` に付ける**。`main` の padding を固定値で設定：
  - `paddingTop = 20`（`Space/lg` にバインド）
  - `paddingBottom = 120`（タブ回避の固定値。DS変数に無いので生値のままで可＝唯一の例外）
  - `paddingLeft = paddingRight = 20`（`Space/lg` にバインド）
- **`wrapper-M` には padding を一切付けない（上下左右すべて 0）**。余白は全て `main` が担当。wrapper にも付けると**二重余白**になる。
- `wrapper-M` は **section 間の `itemSpacing`(gap) のみ** を持ち、これも `Space/*`（例：`Space/3xl`=40）にバインド。
- section / block / group 内部の gap や padding も `Space/*` にバインド。
- 角丸は `Radius/*` にバインド（カードは概ね `Radius/xl`=16 / `Radius/lg`=12、小要素は `Radius/md`=8）。
- 枠線の太さは `BorderWidth/*` にバインド（細`Subtle`=1 / 標準`Default`=1.5 / 太`Strong`=2）。枠線色は `Border/Default|Subtle|Strong`。
- canonical な雛形：`main`: pt=pl=pr=`Space/lg`(20) / pb=120、`wrapper-M`: padding 上下左右すべて 0 / gap=`Space/3xl`(40)。
## ボタンの置き方 ※重要
- **ボタンが1個（単体）の場合は専用の囲み block を作らない**。`block_buttons` 等で包まず、`wrapper-M` 直下にボタンを置く。
- **余計な `paddingTop` を付けない**。ボタン上の間隔は `wrapper-M` の `itemSpacing`（section と同じ DS gap）で取る。囲み frame 側に独自の上余白を足さない。
- **2個以上**（縦/横）並ぶ場合のみ、まとめる block で囲んでよい。その場合も **block 自体に余白(padding)は付けない**。ボタン同士の間隔は block の `itemSpacing` を `Space/*` にバインドして取る。
- ボタンを全幅にするには autolayout 親内で `btn.layoutSizingHorizontal="FILL"`（不可なら `layoutAlign="STRETCH"`）。
## レイアウト方式（重要）
- **内容が短い画面（ボタンを最下部固定）**：フレーム `primaryAxisSizingMode="FIXED"` + `resize(375,812)`、`main.layoutGrow=1`、`wrapper-M` を `layoutGrow=1` + `primaryAxisAlignItems="SPACE_BETWEEN"` にして section=上 / ボタン=下。横paddingは main、wrapper-M横padding=0。
- **内容が長い画面（縦に伸ばす）**：フレーム `primaryAxisSizingMode="AUTO"`（内容に合わせて伸長）。
- **タブバー有りの画面**：タブは“絶対配置で浮いている”ため main 下端に被る。`main.paddingBottom≈95〜120`（タブ79+余白）で回避。フレームAUTO高さの場合はタブの `y` を `frame.height - tab.height` に再設定して最下部へピン留め。
## レイヤー命名規約
`main > wrapper-M > section_◯ > block_◯ > group_◯ > 個別`
- prefix は `section_/block_/group_`。階層飛ばし禁止、block in block / block in group 禁止。
- `header` / `tab_navigation` は main の外。**CTAボタンが単体なら独自 block で包まない**（複数並ぶ時のみ block 可・余白なし）。
- **余白は main が担当（pt/pl/pr=Space/lg(20)、pb=120）。wrapper-M は padding 0（四辺）・gapのみ。**
## DS トークン早見表（ダークモード）
### 色（参考値。実装は必ず下の変数IDにバインド）
- Surface: Primary `#191919` / Secondary・Elevated `#252525` / Tertiary `#4D4D4D`
- Text: Primary `#FFFFFF` / Secondary `#999999` / Tertiary `#4D4D4D` / Link `#1E73DC` / OnBrand(白)
- Brand: Primary(オレンジ) `#F1890E` / Secondary(ネイビー) `#092846`
- Status: Success `#32D74B` / Error `#F0295D` / Warning `#DBA911`
- Font: Noto Sans JP（Regular / Medium / Bold）
### 色 変数ID（作業ファイル R444… 内。別ファイルでは search_design_system / importVariableByKeyAsync で解決）
- Text/Primary `VariableID:832f523ad5505ae3be2c655ae4e0ab84b8825e95/643:0`
- Text/Secondary `VariableID:9e5a00614d8fdada9c7d0778cbec07bbfb83f82a/81:17`
- Text/Link key `cb2207637c76b84acd6b223f69db2cf8e4d60b6c`（importVariableByKeyAsync で取得）
- Brand/Primary `VariableID:8345449add9c27dc030beabcb973e1f61fd6fad1/81:5`
- Status/Error `VariableID:1eb7bd7915dcef65f6d533fa69ade215b9fa13d5/640:14`
- Border/Default `VariableID:1b738a06bcfd3c04f7d5d6eae86d667248ec288d/81:38`（key `1b738a06bcfd3c04f7d5d6eae86d667248ec288d`）
- Border/Subtle key `48a932c9107480e6855a1000dc9a6faf1d7e2228` / Border/Strong key `7b2262bd204511b68c179e087112bd0a4a066459`
- Surface/Secondary key `81b96c071e5e7da7a11a5576e512fc4e8dce5b2f`（importVariableByKeyAsync で取得）
- Surface/Tertiary key `fd1da1cb9253efce25ef07f41429c3fde58da8fa`
### Spacing 変数（"Design System - APP" / コレクション `Spacing`）※padding・gap は必ずこれにバインド
| name | px | VariableID（R444…内） | key（別ファイル用） |
|---|---|---|---|
| Space/xxs | 4 | `VariableID:0a95bbbadd38050296a7dab7bb519b053247250d/89:19` | `0a95bbbadd38050296a7dab7bb519b053247250d` |
| Space/xs | 6 | `VariableID:a365c3b3f793126b9280cbb38ac01fbca242bd7c/89:21` | `a365c3b3f793126b9280cbb38ac01fbca242bd7c` |
| Space/sm | 8 | `VariableID:f06b929889c3f640fab2a0cdf89854c2b3c868ae/89:23` | `f06b929889c3f640fab2a0cdf89854c2b3c868ae` |
| Space/sm-plus | 10 | `VariableID:cc54f0732f1aea7d02b54f92236166ffa4ff85a7/89:25` | `cc54f0732f1aea7d02b54f92236166ffa4ff85a7` |
| Space/md | 12 | `VariableID:e6d690726699aeddf8e8c74e1199629f83f4a1a8/89:27` | `e6d690726699aeddf8e8c74e1199629f83f4a1a8` |
| Space/base | 16 | `VariableID:89d015a41d647ae1d0c696e371971b7589c688b8/89:29` | `89d015a41d647ae1d0c696e371971b7589c688b8` |
| Space/lg | 20 | `VariableID:320f7dcf753fba082955f6183697331b1135ed17/89:31` | `320f7dcf753fba082955f6183697331b1135ed17` |
| Space/xl | 24 | `VariableID:9fd93e78a2e6432a2ded1414005c5b65ceeda5f2/89:33` | `9fd93e78a2e6432a2ded1414005c5b65ceeda5f2` |
| Space/2xl | 32 | `VariableID:5b69b682dbdfc89c7f6ba046b2c0da00c0eba488/89:35` | `5b69b682dbdfc89c7f6ba046b2c0da00c0eba488` |
| Space/3xl | 40 | `VariableID:ef401cd6b5643f8604c4f5c83a61685d68d4829d/619:10` | `ef401cd6b5643f8604c4f5c83a61685d68d4829d` |
- 横padding(main)=Space/lg(20)、section間gap(wrapper-M)=Space/3xl(40) が標準。
### Radius 変数（"Design System - APP" / コレクション `Radius`）※cornerRadius は必ずこれにバインド
| name | px | VariableID（R444…内） | key（別ファイル用） |
|---|---|---|---|
| Radius/sm | 4 | `VariableID:f55bc2d826c9e150f0bb6e295b5ab5f7282e1773/89:3` | `f55bc2d826c9e150f0bb6e295b5ab5f7282e1773` |
| Radius/md | 8 | `VariableID:3739ebeede5e6dc7246a3dddbcc189f3bbb842c0/89:5` | `3739ebeede5e6dc7246a3dddbcc189f3bbb842c0` |
| Radius/lg | 12 | `VariableID:d19e867f0cd2feddd0709e4c08f9add6156f5e9c/89:7` | `d19e867f0cd2feddd0709e4c08f9add6156f5e9c` |
| Radius/xl | 16 | `VariableID:ea41d9c17fdd8cf001d6fe7767cf27bef23336d5/89:9` | `ea41d9c17fdd8cf001d6fe7767cf27bef23336d5` |
| Radius/full | 9999 | `VariableID:aabe2ac8b46207c889a72efe3a5acb74d75b5ba5/89:15` | `aabe2ac8b46207c889a72efe3a5acb74d75b5ba5` |
- 追加（ファイル未読込なら importVariableByKeyAsync で取得）：Radius/2xl(24) key `e5a413fe250d74e88d17ed61ec18d23094ebc374` / Radius/3xl(32) key `ec0b4969367ac5990c4aaf8a349c9ad76baf2c2e` / Radius/4xl(40) key `70704228625fa98fcf3c0b108fe7a50cb5658ba2`
### BorderWidth 変数（"Design System - APP" / コレクション `BorderWidth`）※strokeWeight は必ずこれにバインド
| name | px | VariableID（R444…内） | key（別ファイル用） |
|---|---|---|---|
| BorderWidth/Subtle | 1 | `VariableID:584e7c38d7142a1e92e9af3b406b71038103b943/1542:3` | `584e7c38d7142a1e92e9af3b406b71038103b943` |
| BorderWidth/Default | 1.5 | `VariableID:4958b6fe28f70138101702093320b3bb1eeb9456/1542:5` | `4958b6fe28f70138101702093320b3bb1eeb9456` |
| BorderWidth/Strong | 2 | `VariableID:3684d03e9c5d4c44b2d80915b1fc7b6617295fad/1542:7` | `3684d03e9c5d4c44b2d80915b1fc7b6617295fad` |
- 通常の枠線=`Subtle`(1)、入力/選択枠=`Default`(1.5)、強調/選択中=`Strong`(2)。
### DS テキストスタイル（`await node.setTextStyleIdAsync(id)`）
- subtitle-l(16) `S:f7bdd2b4203a10755196e91046d4da3dec1dc697,283:106`
- subtitle-m(14) `S:85986b330b4cbcb8619d6ce51de898309fbcc24d,283:107`
- title-s(18) `S:cd4411a589d3cd3ff0b0873a34afb1b98a3d9ad7,283:105`
- body-m-strong(14) `S:216b416d6ce36f6dc2fc25b54fb733bb9e2f36c3,283:111`
- caption-l(12) `S:42e27fe6159d00d1071acb7bc97852cbf5d01590,283:118`
### Button コンポーネント（"Design System - APP"、component_set key `1e97d8273706cc74492b235ef7995c509d49da59`）
- Variant: `Primary`(オレンジ) / `Secondary`(白枠・透明) / `Tertiary`(グレー) / `Ghost`(透明) / `Danger` / `Gradient`
- Size: `XL`/`L`/`M`/`S`、State: `Default`/`Loading`/`Disabled`、IconLeft/IconRight: Boolean
- **白地×濃色文字のバリアントは無い**。主CTA=Primary、副=Secondary、無効/控えめ=Tertiary。
- ラベル: `setProperties({ "Label#973:92": "ラベル", "Variant": "Primary", "Size":"L", "IconLeft#973:90":false, "IconRight#973:91":false })`
- 反映されない時は内部 `Label` テキストを直接 `setCharacters`（上書き残り対策）。
- **単体なら囲み block 不要。複数並ぶ時のみ block 可（余白は付けない／間隔は itemSpacing を Space/* にバインド）。**
### Icon コンポーネント
- COMPONENT_SET `10759:4425`、INSTANCE_SWAP プロパティ `Name#438:30`、VARIANT `Size`（値: `xs`/`s`/`m`/`l`/`xl`/`2xl`）
- グリフは "Design System - APP" の各アイコン COMPONENT を `importComponentByKeyAsync(key)` してから swap。例：`general / add` key `cb385b057f77f59ea9a05bd4718ce09e51e56e12` / `navigation / chevron-down` key `31709b74f5f03342ded09dc4d670e9242e9bb159`
- 生成: `iconSet.defaultVariant.createInstance()` → `inst.setProperties({ "Size":"l", "Name#438:30": glyph.id })`
- 色は**内側 VECTOR の fill**にDS変数をバインド。
## use_figma 実装パターン & 落とし穴
~~~js
// 色バインド（opacity 維持）
const paint = figma.variables.setBoundVariableForPaint(
  { type:"SOLID", color:{r:1,g:1,b:1} }, 'color', colorVar);
node.fills = [paint];
// 枠線：色は Border 変数、太さは BorderWidth 変数にバインド（生数値禁止）
node.strokes = [figma.variables.setBoundVariableForPaint(
  { type:"SOLID", color:{r:1,g:1,b:1} }, 'color', borderColorVar)];
node.setBoundVariable('strokeWeight', borderWidthVar); // 例: BorderWidth/Strong(2)
// node.dashPattern=[5,4]; // 破線にする場合のみ
// 余白・gap・角丸を変数にバインド（生数値禁止）
const sp = (id)=>figma.variables.getVariableByIdAsync(id); // 同ファイル
const vSpaceLg  = await sp("VariableID:320f7dcf753fba082955f6183697331b1135ed17/89:31"); // 20
const vSpace3xl = await sp("VariableID:ef401cd6b5643f8604c4f5c83a61685d68d4829d/619:10"); // 40
const vRadiusXl = await sp("VariableID:ea41d9c17fdd8cf001d6fe7767cf27bef23336d5/89:9");   // 16
const vBwStrong = await sp("VariableID:3684d03e9c5d4c44b2d80915b1fc7b6617295fad/1542:7"); // 2
// 余白は main に。pt/pl/pr=Space/lg(20)、pb=120(固定/タブ回避)
main.setBoundVariable('paddingTop',   vSpaceLg);
main.setBoundVariable('paddingLeft',  vSpaceLg);
main.setBoundVariable('paddingRight', vSpaceLg);
main.paddingBottom = 120;                               // DS変数に無い固定値（唯一の例外）
// wrapper-M は padding 一切なし（上下左右すべて0）
wrap.paddingTop = 0; wrap.paddingBottom = 0; wrap.paddingLeft = 0; wrap.paddingRight = 0;
wrap.setBoundVariable('itemSpacing', vSpace3xl);        // section間gap のみ
// 角丸（一律）は4隅をバインド
for (const f of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])
  card.setBoundVariable(f, vRadiusXl);
// 別ファイルは key から：const v = await figma.variables.importVariableByKeyAsync(key);
// テキスト生成（必ず先に loadFontAsync）
for (const w of ["Regular","Medium","Bold"])
  await figma.loadFontAsync({ family:"Noto Sans JP", style:w });
// GROUP は fills getter が throw → try/catch で読む
const safe=(n,p)=>{try{const v=n[p];return Array.isArray(v)?v:null;}catch(e){return null;}};
// counterAxisAlignItems に "STRETCH" は不可。子を全幅にするには子側 layoutAlign="STRETCH"
// 部分的な色変え（赤強調など）
const i=t.characters.indexOf("強調語");
t.setRangeFontName(i,i+n,{family:"Noto Sans JP",style:"Bold"});
t.setRangeFills(i,i+n,[redPaint]);
// モーダル：オーバーレイは layoutMode 設定後に sizing を FIXED 化してから resize
ov.layoutMode="VERTICAL"; ov.primaryAxisSizingMode="FIXED"; ov.counterAxisSizingMode="FIXED";
ov.resize(375,812); ov.primaryAxisAlignItems="CENTER"; ov.counterAxisAlignItems="CENTER";
ov.layoutPositioning="ABSOLUTE"; ov.x=0; ov.y=0;
~~~
- **深い getNodeByIdAsync ツリー読み取りはタイムアウトしやすい** → 直下の子だけ読む / 必要なノードIDを狙って読む。
- **get_screenshot はキャッシュ/遅延あり**。ラベル等が古く見えても `componentProperties`・内部 `characters`・`boundVariables` を読めば実体が正しいか判定できる。
- 自己ノードへの reaction はエラーになるのでスキップ。
## 検証チェックリスト
- [ ] テキストは参考と同一（改行含む）
- [ ] 色・テキストが全てDS変数/スタイルにバインド（生HEX残り無し）
- [ ] **余白(padding/gap)・角丸・線幅(strokeWeight)が全てDS変数(Spacing/Radius/BorderWidth)にバインド（生数値残り無し）**
- [ ] **wrapper-M に padding が一切無い（上下左右すべて0）。余白は main 側（pt/pl/pr=Space/lg(20)、pb=120）**
- [ ] **ボタン単体は囲んでいない／複数並ぶ時のみ block で囲み、余計な余白(padding)が無い**
- [ ] アイコンは Icon インスタンス（直置きグリフ0）
- [ ] ボタンは Primary/Secondary/Tertiary を適切に
- [ ] タブバーの有無が参考と一致、main 下padding でボタンが被らない
- [ ] レイヤー名が規約準拠
## Cowork での依頼の出し方（例）
- 「fileKey `R444…` の `13354-11890` を、参考 `13354-10148` に合わせて修正して。テキストは同じ、レイアウトはDSで。」
- 「`13354-12626`〜`13354-13058`(Step2系)を参考 `…` に合わせて順に作って。タブバーは参考準拠で。」
- 「この画面のボタンを Primary/Secondary に、色・余白・角丸・線幅を全部DS変数にバインドして。」
