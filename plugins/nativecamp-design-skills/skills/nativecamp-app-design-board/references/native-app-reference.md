# Native APP case — repos + reference-code block

Most NativeCamp app work has shipped as a **Webview** inside the native shell,
so **there have been no Native-APP (fully native screen) cases yet**. But some
jobs *will* be built as native iOS / Android screens rather than a Webview. When
that's the case, do two extra things.

## 1. Reference the real native codebases
When the design is going to be implemented as a **Native APP** (not a Webview),
read these to match existing components, navigation, and naming instead of
inventing new ones:
- iOS — https://github.com/VJSOL/NativeCamp-iOS
- Android — https://github.com/VJSOL/NativeCamp-Android

Use them to check whether a "net-new" component already exists, to reuse the
real view/coordinator names in the Implementation notes, and to keep tokens
(colors / type / radius) consistent with what the app already ships.

## 2. Add a "参考コード — カウントアップ＋ポップ（iOS / Android）" section
For a **Native APP** case, add a reference-code block **immediately before the
Implementation notes section** so developers get a concrete, copy-pasteable
starting point for any signature animation/interaction the screen needs
(the count-up + pop coupon hero is the canonical example). Prefix the section
with a clear "**もしNative APPの場合**" / "**If this is a Native APP build**"
note so it's obvious the block only applies to native (not Webview) work.

Adapt the specific dials (target value, easing, durations) to the actual screen;
the structure below is the pattern to follow. Paste this markup as-is (it uses
the board's existing `.codelbl` label style — add the small rule below if the
board doesn't already have it).

```css
/* label above each code block (add once if not already present) */
.codelbl{font-family:var(--mono);font-size:12px;font-weight:700;color:var(--ink-soft);
  margin:16px 0 6px}
.board pre{background:#0d0d0d;color:#e6e6e6;border-radius:12px;padding:16px 18px;
  overflow:auto;font-family:var(--mono);font-size:12.5px;line-height:1.55;margin:0}
.board pre code{white-space:pre}
```

```html
<!-- ===== 参考コード — only for a Native APP build (not Webview) ===== -->
<h4>参考コード — カウントアップ＋ポップ（iOS / Android）
  <span style="font-weight:500;color:var(--ink-soft)">／ もしNative APPの場合</span></h4>
<ul>
  <li>両OS共通の値：カウントアップ 0→値 約1000ms OutExpo／ポップ スケール
    0.72→1.16→0.94→1.0（約700ms）＋発光／対象は利用可能クーポンのヒーローのみ／
    Reduce Motion対応／出現時に1回。</li>
</ul>

<div class="codelbl">Swift · SwiftUI</div>
<pre><code>import SwiftUI

// 0 → value, animated per-frame via Animatable
struct AnimatedNumber: View, Animatable {
    var value: Double
    var animatableData: Double { get { value } set { value = newValue } }
    var body: some View {
        Text(value, format: .number.precision(.fractionLength(0)))  // grouping
            .monospacedDigit()                                       // tabular-nums
    }
}

struct CouponHero: View {
    let target: Int
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var shown = 0.0
    @State private var popped = false
    @State private var glow = false

    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 6) {
            AnimatedNumber(value: shown).font(.system(size: 38, weight: .bold))
            Text("available").font(.system(size: 19, weight: .bold))   // localized
        }
        .foregroundStyle(Color(red: 1, green: 0.58, blue: 0))          // ≈ #FF9500
        .scaleEffect(popped ? 1.0 : 0.72)
        .shadow(color: .orange.opacity(glow ? 0.6 : 0), radius: glow ? 18 : 0)
        .onAppear(perform: play)
    }

    private func play() {
        guard !reduceMotion else { shown = Double(target); popped = true; return }
        shown = 0; popped = false; glow = false
        withAnimation(.timingCurve(0.16, 1, 0.3, 1, duration: 1.0)) { shown = Double(target) }
        withAnimation(.spring(response: 0.4, dampingFraction: 0.55)) { popped = true }
        withAnimation(.easeOut(duration: 0.18)) { glow = true }
        withAnimation(.easeIn(duration: 0.5).delay(0.18)) { glow = false }
    }
}</code></pre>

<div class="codelbl">Kotlin · Jetpack Compose</div>
<pre><code>val OutExpo = Easing { t -&gt; if (t &gt;= 1f) 1f else 1f - 2f.pow(-10f * t) }

@Composable
fun CouponHero(target: Int, reduceMotion: Boolean) {
    var play by remember { mutableStateOf(false) }
    val value by animateIntAsState(
        targetValue = if (play) target else 0,
        animationSpec = if (reduceMotion) snap() else tween(1000, easing = OutExpo)
    )
    val scale by animateFloatAsState(
        targetValue = if (play) 1f else 0.72f,
        animationSpec = if (reduceMotion) snap()
                        else spring(dampingRatio = 0.55f, stiffness = Spring.StiffnessMediumLow)
    )
    LaunchedEffect(Unit) { play = true }             // once per appearance

    Text(
        "%,d".format(value),                         // grouping
        fontSize = 38.sp, fontWeight = FontWeight.Bold,
        color = Color(0xFFFF9500),
        modifier = Modifier.graphicsLayer { scaleX = scale; scaleY = scale }
    )
}</code></pre>

<div class="codelbl">Kotlin · classic Views (current NCxAI Android is XML/View-based)</div>
<pre><code>fun animateCoupon(number: TextView, icon: View, target: Int) {
    if (isReduceMotion(number.context)) { number.text = "%,d".format(target); return }

    ValueAnimator.ofInt(0, target).apply {                       // count-up
        duration = 1000
        interpolator = TimeInterpolator { t -&gt;
            if (t &gt;= 1f) 1f else 1f - 2.0.pow((-10 * t).toDouble()).toFloat()
        }
        addUpdateListener { number.text = "%,d".format(it.animatedValue as Int) }
        start()
    }
    listOf(number, icon).forEach { v -&gt;                          // pop (overshoot)
        AnimatorSet().apply {
            playTogether(
                ObjectAnimator.ofFloat(v, View.SCALE_X, 0.72f, 1.16f, 0.94f, 1f),
                ObjectAnimator.ofFloat(v, View.SCALE_Y, 0.72f, 1.16f, 0.94f, 1f)
            )
            duration = 700
            start()
        }
    }
}

fun isReduceMotion(ctx: Context) =
    Settings.Global.getFloat(ctx.contentResolver, Settings.Global.ANIMATOR_DURATION_SCALE, 1f) == 0f</code></pre>

<ul>
  <li><b>注意1</b> — 出現時に1回のみ発火。残高更新の度に発火させない（Web復帰後に再ポップしてしまう）。</li>
  <li><b>注意2</b> — Reduce Motion対応必須：iOS <code>accessibilityReduceMotion</code>、
    Android <code>ANIMATOR_DURATION_SCALE == 0</code> → 最終値へ即時。</li>
</ul>
<!-- ===== /参考コード ===== -->
```

Then the **Implementation notes** section follows (per-platform view / coordinator
names, palette, type) — with the native names verified against the two repos above.
