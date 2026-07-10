# NCxAI design system — dark-mode app screens

The NativeCamp Japanese-learning app UI is **dark mode only**, accent orange.
Reproduce screens faithfully with these tokens (from Figma variables).

## Color
| Token | Value | Use |
|---|---|---|
| Brand / Primary | `#f1890e` | primary buttons, accents, progress fill, links inside app chrome |
| Brand gradient | `linear-gradient(90deg,#FF6B35,#EEB633)` | plan-card header, trial badge text, timeline dots/line |
| App background | `#0d0d0d` | splash / value-prop / trial-started base (under the glow) |
| Surface / Primary | `#1a1a1a` | default screen background (questions, sign up, login) |
| Surface / Secondary | `#333333` | option rows, plan body, "casually" card |
| Surface / Tertiary | `#4d4d4d` | progress track (off), schedule box |
| Text / Primary | `#ffffff` | headings, body on dark |
| Text / Secondary | `#999999` | subtitles, captions, hints |
| Text / Tertiary | `#4d4d4d` | input placeholders |
| Text / Link | `#1e73dc` | "Already have an account? Log in" |
| Border default | `rgba(255,255,255,.1)` | dividers, ghost buttons, schedule inner border |
| Border strong | `rgba(255,255,255,.2)` | inputs, "casually" card border |
| Border subtle | `rgba(255,255,255,.05)` | hairline under footer links |

## Type — Noto Sans JP
| Style | size / weight / line-height |
|---|---|
| Heading S (screen title) | 24 / 700 / 1.4 |
| Subtitle L, Button L | 16 / 700 · 500 / 1.3–1.5 |
| Body M | 14 / 400 / 1.5 |
| Caption L (field labels) | 12 / 500 / 1.25 |
| Caption M (hints) | 10 / 500 / 1.3 |
| Heading M ($ amount) | 28 / 700 / 1.2 |

## Radius / Spacing / Sizes
- Radius: `md 8` · `lg 12` · `xl 16` · `2xl 24` · `full 9999`
- Spacing scale: `4 6 8 10 12 16 20 24 40 64`
- Button 48h (L) / 56h (XL) · Option 53h · Input 44h (border 1.5px) · Progress 4h

## Backgrounds by screen (group differences)
- **Splash / value-prop**: dark + warm orange glow (export the Figma bg image, or CSS radial-gradient blobs of `rgba(241,137,14,…)` on `#0d0d0d`).
- **Questions / Sign up**: flat `#1a1a1a` (no glow).
- **Trial started**: warm brown gradient `linear-gradient(180deg,#3a2412,#241610 42%,#130d08)` + small top glow.
- **Log in / Tutor**: **A group = warm glow, B group = flat `#1a1a1a`** (group theme differs; measurement excludes these screens).

---

## Reusable phone-frame CSS component library

Drop this `<style>` into the board once. Every screen is a `.phone` (a fixed
375px device frame; the content inside is fluid and follows the frame). The
board itself is a light "design tool" canvas so the dark screens pop.

```css
/* ---- board (light canvas) ---- */
:root{--board:#eceef2;--panel:#fff;--ink:#16181d;--ink-soft:#4b5159;--muted:#8b919b;
  --rule:#e0e3e9;--rule-soft:#eef0f4;--accent:#f1890e;
  --shadow:0 1px 2px rgba(16,18,29,.05),0 6px 20px rgba(16,18,29,.06);
  --shadow-phone:0 14px 44px rgba(16,18,29,.22);
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Kaku Gothic ProN","Noto Sans JP",sans-serif;}
*{box-sizing:border-box} body{margin:0}
.board{background:var(--board);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.6;
  -webkit-font-smoothing:antialiased;padding:clamp(20px,4vw,56px) clamp(14px,3vw,44px)}
.wrap{max-width:1500px;margin:0 auto}
.sec-head{display:flex;align-items:baseline;gap:12px;margin:0 0 22px;padding-bottom:12px;border-bottom:2px solid var(--rule)}
.sec-head .n{font-family:var(--mono);font-size:12px;font-weight:700;color:#fff;background:var(--ink);border-radius:7px;padding:3px 9px;align-self:center}
.sec-head h2{font-size:19px;font-weight:800;letter-spacing:-.01em;margin:0}
.sec-head .k{font-size:12.5px;color:var(--muted);margin-left:auto;text-align:right}
.rail{display:flex;flex-wrap:wrap;gap:40px 34px;align-items:flex-start}
.screen{width:375px}
.screen figcaption{margin:16px 3px 0}
.screen .cap-t{display:flex;align-items:center;gap:9px;margin-bottom:5px}
.screen .step-no{font-family:var(--mono);font-size:12px;font-weight:800;color:#fff;background:var(--accent);width:24px;height:24px;border-radius:7px;display:grid;place-items:center;flex:none}
.screen .cap-t b{font-size:15px;font-weight:800}
.screen .nid{font-family:var(--mono);font-size:10.5px;color:var(--muted);margin-left:auto}
.screen .cap-d{font-size:12.5px;color:var(--ink-soft);margin:0}

/* ---- phone (dark app) ---- */
.phone{--brand:#f1890e;--s1:#1a1a1a;--s2:#333;--s3:#4d4d4d;--white:#fff;--sec:#999;--ter:#4d4d4d;--link:#1e73dc;
  --b-default:rgba(255,255,255,.1);--b-strong:rgba(255,255,255,.2);--b-subtle:rgba(255,255,255,.05);
  width:375px;min-height:812px;flex:none;position:relative;overflow:hidden;background:var(--s1);color:var(--white);
  border-radius:40px;box-shadow:var(--shadow-phone);border:1px solid #050505;font-family:"Noto Sans JP",var(--sans);
  display:flex;flex-direction:column;background-size:cover;background-position:center}
.phone.tall{min-height:0}
.phone *{box-sizing:border-box}
.warm{background:radial-gradient(200px 170px at 88% 4%,rgba(241,137,14,.30),transparent 68%),linear-gradient(180deg,#3a2412 0%,#241610 42%,#130d08 100%)}
.z{position:relative;z-index:1}
.sb{height:42px;display:flex;align-items:center;justify-content:space-between;padding:0 15px 0 25px;flex:none}
.sb .t{font-size:15px;font-weight:600;letter-spacing:.2px}
.sb .sbr{height:12px;width:68px;display:block}
.appbar{height:44px;display:flex;align-items:center;justify-content:center;position:relative;flex:none}
.appbar .ttl{font-size:16px;font-weight:700;line-height:1.5}
.appbar .back{position:absolute;left:20px;top:50%;transform:translateY(-50%);width:24px;height:24px}
.appbar .back img{width:24px;height:24px;display:block}
.prog{display:flex;gap:8px}
.prog .seg{height:4px;flex:1;border-radius:9999px;background:var(--s3)}
.prog .seg.on{background:var(--brand)}
.h1s{font-size:24px;line-height:1.4;font-weight:700;margin:0;letter-spacing:-.005em}
.subs{font-size:14px;line-height:1.5;color:var(--sec);margin:0}
.btn{display:flex;align-items:center;justify-content:center;gap:8px;height:48px;border-radius:9999px;border:none;width:100%;
  font-family:"Noto Sans JP",var(--sans);font-size:16px;font-weight:500;line-height:1.3}
.btn-pri{background:var(--brand);color:#fff}
.social{position:relative;display:flex;align-items:center;justify-content:center;height:48px;border-radius:9999px;width:100%;
  border:1.5px solid var(--b-default);background:transparent;color:#fff;font-family:"Noto Sans JP",var(--sans);font-size:16px;font-weight:500}
.social .ico{position:absolute;left:12px;top:50%;transform:translateY(-50%);width:20px;height:20px;display:flex;align-items:center;justify-content:center}
.social .ico img,.social .ico svg{width:20px;height:20px;display:block}
.opt{display:flex;align-items:center;min-height:53px;background:var(--s2);border:1px solid var(--b-default);border-radius:12px;padding:0 16px;font-size:15px;font-weight:500;color:var(--white)}
.flabel{font-size:12px;font-weight:500;color:var(--sec);margin:0 0 6px;line-height:1.25}
.field{height:44px;border:1.5px solid var(--b-strong);border-radius:8px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;gap:8px}
.field .ph{color:var(--ter);font-size:14px;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.field .val{color:#fff;font-size:14px;flex:1}
.field .act{color:var(--sec);font-size:12px;font-weight:500}
.field .eye{width:24px;height:24px;display:block}
.fhint{font-size:10px;color:var(--sec);margin:6px 0 0;font-weight:500}
.divider{display:flex;align-items:center;gap:12px;color:var(--sec);font-size:13px}
.divider::before,.divider::after{content:"";height:1px;flex:1;background:var(--b-default)}
.dots{display:flex;gap:8px;justify-content:center}
.dots i{width:8px;height:8px;border-radius:50%;background:var(--s3)}
.dots i.on{background:var(--brand)}
.swipe{flex:1;display:flex;flex-direction:column} /* group hero+text+dots = one swipe/pager region */
.linkc{color:var(--link);font-size:14px;font-weight:500}
.tutor{color:var(--sec);font-size:12px;text-decoration:underline;text-underline-offset:2px}
.hair{height:1px;background:var(--b-subtle)}
.hero{width:100%;height:200px;object-fit:cover;border-radius:24px;display:block}
.herocard{width:100%;height:200px;border-radius:24px;display:flex;align-items:flex-end;justify-content:center;overflow:hidden;background-size:cover;background-position:center}
.logo{width:200px;height:29.27px;display:block}
/* plan card + trial timeline (payment screen) */
.plan{border-radius:16px;overflow:hidden;width:100%}
.plan-h{background:linear-gradient(90deg,#ff6b35 0%,#eeb633 100%);display:flex;align-items:center;gap:6px;padding:12px 16px}
.plan-h .crown{width:24px;height:24px;display:block}
.plan-h .pt{flex:1;font-size:18px;font-weight:700;line-height:1.4;color:#fff;text-shadow:0 5px 15px rgba(0,0,0,.15)}
.plan-h .badge{background:#fff;border-radius:9999px;padding:4px 12px;box-shadow:0 3px 10px rgba(0,0,0,.1);font-size:12px;font-weight:500}
.plan-h .badge b{background:linear-gradient(90deg,#ff6b35,#eeb633);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;font-weight:500}
.plan-b{background:var(--s2);padding:20px;display:flex;flex-direction:column;gap:24px}
.prow{display:flex;align-items:center;gap:12px}
.prow .lab{font-size:14px;color:var(--sec)} .prow .fill{flex:1;border-top:1px dashed rgba(255,255,255,.28)}
.prow .big{font-size:28px;font-weight:700;line-height:1.2;color:#fff} .prow .amt{font-size:14px;font-weight:500;color:var(--sec)}
.sched{background:var(--s3);border:2px solid var(--b-default);border-radius:8px;padding:20px;display:flex;flex-direction:column;gap:16px}
.sched h4{margin:0;font-size:16px;font-weight:700;line-height:1.2} .sched .rule{height:1px;background:var(--b-default)}
/* timeline: connector line spans ONLY dot->dot (never overflows below the last dot) */
.tl{display:flex;flex-direction:column}
.tl .row{display:flex;gap:12px}
.tl .dotcol{width:10px;flex:none;align-self:stretch;position:relative}
.tl .dot{position:absolute;top:4px;left:0;width:10px;height:10px;border-radius:50%;background:linear-gradient(180deg,#ff6b35,#eeb633)}
.tl .line{position:absolute;top:9px;left:4px;width:2px;height:100%;background:linear-gradient(180deg,#ff6b35,#eeb633)}
.tl .rowc{padding-bottom:20px} .tl .row:last-child .rowc{padding-bottom:0}
.tl .rowc b{font-size:14px;font-weight:500;color:#fff;display:block;line-height:1.2}
.tl .rowc small{font-size:13px;color:var(--sec);display:block;margin-top:6px;line-height:1.2}
/* Apple Pay (white/black) + Google Pay buttons */
.applepay{background:#fff;border:1px solid #000;color:#000;height:50px;border-radius:100px;width:100%;display:flex;align-items:center;justify-content:center;gap:5px;font-family:-apple-system,"SF Pro Text",sans-serif;font-weight:600;font-size:22px;letter-spacing:-.5px}
.applepay img{width:20px;height:24px;display:block}
.gpay{background:#fff;border:1px solid #000;color:#000;height:50px;border-radius:100px;width:100%;display:flex;align-items:center;justify-content:center;gap:2px;font-weight:700;font-size:20px}
.gpay svg{height:22px;width:auto;display:block}
/* WorldPay placeholder (hosted form is rendered by the SDK, not by us) */
.wp-ph{width:100%;aspect-ratio:335/500;border:1.5px dashed rgba(255,255,255,.3);border-radius:14px;background:rgba(255,255,255,.03);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;gap:8px}
.wp-ph .t{font-size:14px;font-weight:700;color:#fff} .wp-ph .d{font-size:12px;color:var(--sec);line-height:1.5;max-width:230px}
.wp-ph .tag{font-family:var(--mono);font-size:10px;color:var(--sec);border:1px solid var(--b-default);border-radius:5px;padding:2px 8px;margin-top:4px}
/* one-card benefits + photo block */
.casually{background:var(--s2);border:2px solid var(--b-strong);border-radius:16px;padding:2px;overflow:hidden}
.casually .tx{padding:24px 24px 0;display:flex;flex-direction:column;gap:20px}
.casually h3{margin:0;font-size:24px;font-weight:700;line-height:1.4;color:#fff}
.blist{display:flex;flex-direction:column;gap:8px}
.blist .it{display:flex;gap:16px;align-items:flex-start} .blist .it img{width:24px;height:24px;flex:none}
.blist .it span{flex:1;font-size:14px;font-weight:500;line-height:1.5;color:#fff}
.casually .fig{display:flex;justify-content:center;padding-top:20px}
.casually .fig img{width:100%;max-width:335px;display:block;border-bottom-left-radius:14px;border-bottom-right-radius:14px}
.ends{border:1px solid var(--brand);border-radius:16px;display:flex;align-items:center;justify-content:space-between;padding:14px 20px}
.ends .l{color:var(--brand);font-weight:700;font-size:15px} .ends .r{font-weight:700;font-size:15px}
.lot-char{width:200px;height:200px}
@media(max-width:820px){.screen,.phone{width:340px}}
```

## Status bar (repeat inside each `.phone`, right after the opening tag)
```html
<div class="sb z"><span class="t">10:00</span><img class="sbr" src="{{ASSET:ic_statusbar_right.svg}}" alt=""></div>
```
Splash has **no** status bar (full-bleed logo on the glow).

## Lottie character (screens with the mascot)
Container: `<div id="lottie-x" class="lot-char"></div>` (or a fixed `147x156`
box aligned to the bottom of a `.herocard`). Mount once at the end of the board:
```html
<script>{{LOTTIE_LIB}}</script>
<script>
var WAVE={{LOTTIE_JSON:wave_animation.json}};
var BLINK={{LOTTIE_JSON:wave_blink_animation.json}};
function mk(id,d){var el=document.getElementById(id);
  if(el&&window.lottie){try{lottie.loadAnimation({container:el,renderer:"svg",loop:true,autoplay:true,animationData:d});}catch(e){}}}
mk("lottie-teacher",BLINK); mk("lottie-trial",WAVE);
</script>
```
`mk` no-ops if the container isn't on the page, so the same block is safe for
A (has both) and B (trial only).

See `references/component-snippets.md` for ready-to-paste per-screen markup.
