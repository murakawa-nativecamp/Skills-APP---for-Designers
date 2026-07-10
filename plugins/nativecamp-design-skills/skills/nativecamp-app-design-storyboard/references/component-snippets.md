# Ready-to-paste screen markup

All classes come from `references/design-system.md`. Asset tokens (`{{ASSET:…}}`,
`{{LOTTIE_*}}`) are resolved by `scripts/inject_assets.py`. Wrap each screen in:

```html
<figure class="screen">
  <div class="phone …">…</div>
  <figcaption>
    <div class="cap-t"><span class="step-no">N</span><b>Title</b><span class="nid">FIGMA:ID</span></div>
    <p class="cap-d">One-line overview (no implementation detail).</p>
  </figcaption>
</figure>
```
Captions: English, overview only. Group screens in `.rail` inside a `.sec-head` section.

## Inline brand glyphs (Figma can't export these — see figma-workflow.md)
Google "G" (use in social buttons / Google Pay):
```html
<svg viewBox="0 0 18 18" width="20" height="20"><path fill="#4285F4" d="M17.6 9.2c0-.6-.05-1.2-.15-1.7H9v3.3h4.8a4.1 4.1 0 01-1.8 2.7v2.2h2.9c1.7-1.6 2.7-3.9 2.7-6.5z"/><path fill="#34A853" d="M9 18c2.4 0 4.5-.8 6-2.2l-2.9-2.2c-.8.5-1.8.9-3.1.9-2.4 0-4.4-1.6-5.1-3.8H.9v2.3A9 9 0 009 18z"/><path fill="#FBBC05" d="M3.9 10.7a5.4 5.4 0 010-3.4V5H.9a9 9 0 000 8l3-2.3z"/><path fill="#EA4335" d="M9 3.6c1.3 0 2.5.5 3.4 1.3L15 2.3A9 9 0 00.9 5l3 2.3C4.6 5.2 6.6 3.6 9 3.6z"/></svg>
```
Apple: export not usable; put a standard Apple silhouette SVG in `img/asset/`
as `ic_apple.svg` (white, `fill` via `var(--fill-0,#fff)`) and `ic_apple_black.svg`
(black, for Apple Pay). Reference them with `{{ASSET:ic_apple.svg}}`.

## Splash (no status bar)
```html
<div class="phone" style="background-image:url('{{ASSET:img_bg_splash.webp}}')">
  <div class="z" style="flex:1;display:grid;place-items:center">
    <img class="logo" src="{{ASSET:logo_nativecamp.svg}}" alt="NativeCamp">
  </div>
</div>
```

## Value-prop / strength (hero→dots = one swipe region; Next has 40px above & below)
```html
<div class="phone" style="background-image:url('{{ASSET:img_bg_strength1.webp}}')">
  <SB/>
  <div class="appbar z"></div>
  <div class="z" style="flex:1;display:flex;flex-direction:column;padding:20px 20px 40px">
    <div class="swipe" data-swipe="carousel">
      <img class="hero" src="{{ASSET:img_strength1_hero.webp}}" alt="">
      <div style="margin-top:24px;display:flex;flex-direction:column;gap:12px;text-align:center">
        <p class="h1s">Just 10 minutes a day, every day</p>
        <p class="subs">Fit a lesson into any spare moment.</p>
      </div>
      <div style="flex:1"></div>
      <div class="dots"><i class="on"></i><i></i><i></i></div>
    </div>
    <button class="btn btn-pri" style="margin:40px 0">Next</button>
    <div style="text-align:center"><span class="linkc">Already have an account? Log in</span></div>
    <div class="hair" style="margin:16px 0"></div>
    <div style="text-align:center"><span class="tutor">Are you working as a tutor?</span></div>
  </div>
</div>
```
Character value-prop: swap the `<img class="hero">` for
`<div class="herocard" style="background-image:url('{{ASSET:img_herocard_teacher.webp}}')"><div id="lottie-teacher" style="width:147px;height:156px"></div></div>`.

## Onboarding question (progress N/4; Continue font = Noto Sans JP Medium; 64px below)
```html
<div class="phone">
  <SB/>
  <div class="appbar z"><span class="back"><img src="{{ASSET:ic_chevron_left.svg}}" alt="back"></span><span class="ttl">About you</span></div>
  <div class="z" style="flex:1;display:flex;flex-direction:column;padding:20px 20px 64px">
    <div class="prog"><span class="seg on"></span><span class="seg"></span><span class="seg"></span><span class="seg"></span></div>
    <div style="margin-top:40px;display:flex;flex-direction:column;gap:12px">
      <p class="h1s">Why are you learning Japanese?</p>
      <p class="subs">3 quick questions — we'll tailor your lessons.</p>
    </div>
    <div style="margin-top:40px;display:flex;flex-direction:column;gap:8px">
      <div class="opt">Travel &amp; living in Japan</div><div class="opt">Work, study &amp; JLPT</div>
      <div class="opt">Anime, manga &amp; culture</div><div class="opt">Just for fun</div>
    </div>
    <div style="flex:1"></div>
    <button class="btn btn-pri">Continue</button>
  </div>
</div>
```

## Sign up (social icon pinned LEFT via .social .ico)
```html
<div class="phone">
  <SB/>
  <div class="appbar z"><span class="ttl">Sign up</span></div>
  <div class="z" style="flex:1;display:flex;flex-direction:column;padding:20px 20px 64px">
    <div style="display:flex;flex-direction:column;gap:24px">
      <div style="display:flex;flex-direction:column;gap:16px">
        <div><p class="flabel">Email address</p><div class="field"><span class="ph">you@example.com</span><span class="act">edit</span></div></div>
        <div><p class="flabel">Password</p><div class="field"><span class="val">&nbsp;</span><img class="eye" src="{{ASSET:ic_visibility_off.svg}}" alt=""></div><p class="fhint">Forgot your password?</p></div>
      </div>
      <button class="btn btn-pri">Continue</button>
      <div class="divider">or</div>
      <div style="display:flex;flex-direction:column;gap:8px">
        <div class="social"><span class="ico"><img src="{{ASSET:ic_apple.svg}}" alt=""></span>Continue with Apple</div>
        <div class="social"><span class="ico"><!-- Google G svg --></span>Continue with Google</div>
      </div>
    </div>
    <!-- Variant B only: Log in / tutor links pinned at the very bottom -->
    <!-- <div style="flex:1"></div>
         <div style="text-align:center"><span class="linkc">Already have an account? Log in</span></div>
         <div class="hair" style="margin:16px 0"></div>
         <div style="text-align:center"><span class="tutor">Are you working as a tutor?</span></div> -->
  </div>
</div>
```

## Card / trial (plan + Apple/Google Pay + WorldPay placeholder + benefits card)
```html
<div class="phone tall">
  <SB/>
  <div class="appbar z"><span class="ttl">Free Trial</span></div>
  <div class="z" style="padding:20px 20px 64px;display:flex;flex-direction:column;gap:40px">
    <div style="display:flex;flex-direction:column;gap:16px">
      <p class="h1s">Let's start the 7‑day free trial right away!</p>
      <p class="subs">If you cancel your membership during the free trial period, there is no monthly fee.</p>
    </div>
    <div class="plan">
      <div class="plan-h"><img class="crown" src="{{ASSET:ic_crown.svg}}" alt=""><span class="pt">Premium Plan</span><span class="badge"><b>7-day free trial</b></span></div>
      <div class="plan-b">
        <div style="display:flex;flex-direction:column;gap:12px">
          <div class="prow"><span class="lab">Today</span><span class="fill"></span><span class="big">$0.00</span></div>
          <div class="prow"><span class="lab">From Day 7</span><span class="fill"></span><span class="amt">$99.00 / month</span></div>
        </div>
        <div class="sched">
          <h4>Your 7-day free trial</h4><div class="rule"></div>
          <div class="tl">
            <div class="row"><div class="dotcol"><span class="dot"></span><span class="line"></span></div><div class="rowc"><b>Today · Jun 30 (Tue)</b><small>You're charged $0 today.</small></div></div>
            <div class="row"><div class="dotcol"><span class="dot"></span></div><div class="rowc"><b>Jul 7 (Tue) · Day 7</b><small>First payment of $99 / month.</small></div></div>
          </div>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:24px">
      <!-- iOS: --> <button class="applepay"><img src="{{ASSET:ic_apple_black.svg}}" alt="">Pay</button>
      <!-- Android variant: <button class="gpay"><!-- Google G 22px --><span style="color:#5f6368;font-weight:700;font-family:Arial">Pay</span></button> -->
      <div class="divider">or</div>
      <div class="wp-ph"><div class="t">WorldPay hosted card form</div><div class="d">Card number, name, expiry &amp; CVC are rendered by WorldPay's hosted fields, styled to match this screen.</div><div class="tag">placeholder — WorldPay design applied</div></div>
    </div>
    <div class="casually">
      <div class="tx"><h3>Let's start a Japanese lesson casually!</h3>
        <div class="blist">
          <div class="it"><img src="{{ASSET:ic_check_circle.svg}}" alt=""><span>Instant Lesson: Unlimited Sessions</span></div>
          <div class="it"><img src="{{ASSET:ic_check_circle.svg}}" alt=""><span>Choose from more than 600 instructors.</span></div>
          <div class="it"><img src="{{ASSET:ic_check_circle.svg}}" alt=""><span>Use more than 500 types of materials for free.</span></div>
        </div>
      </div>
      <div class="fig"><img src="{{ASSET:img_trial_lesson.webp}}" alt=""></div>
    </div>
  </div>
</div>
```

## Trial started (group centered; Trial ends 20px narrower than the button; 64px below button)
```html
<div class="phone warm">
  <SB/>
  <div class="appbar z"><span class="ttl">Free Trial Started</span></div>
  <div class="z" style="flex:1;display:flex;flex-direction:column;padding:20px 20px 64px;text-align:center">
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:32px">
      <div style="display:flex;flex-direction:column;gap:14px">
        <p class="h1s" style="font-size:28px;line-height:1.2">Welcome to<br>NativeCamp!</p>
        <p style="color:var(--brand);font-weight:700;margin:0;font-size:15px">🎉 Your free week starts now 🎉</p>
      </div>
      <div style="display:grid;place-items:center"><div id="lottie-trial" class="lot-char"></div></div>
      <div class="ends" style="margin:0 20px"><span class="l">Trial ends</span><span class="r">Jun 17, 11:59 PM</span></div>
    </div>
    <button class="btn btn-pri">Start learning Japanese</button>
  </div>
</div>
```

## Log in / Tutor (A group = warm-glow bg via background-image; B group = flat, omit background-image)
Log in = Email + Continue + Apple/Google/LINE/Facebook (`{{ASSET:ic_line.svg}}`,
`{{ASSET:ic_facebook.svg}}`). Tutor = メールアドレス + パスワード + パスワードを忘れた場合はこちら + Continue (Japanese, faithful to Figma). Both use a back chevron.

> `<SB/>` above is shorthand — paste the real status-bar `<div class="sb z">…</div>`
> from design-system.md into each screen.
