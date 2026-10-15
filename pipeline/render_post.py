#!/usr/bin/env python3
"""b.wylde post renderer. Turns a JSON spec into Instagram-ready JPGs (1080x1350, story 1080x1920).

Usage:  python3 render_post.py spec.json OUT_DIR
Spec:   {"slides":[{"template":"quote-plum","fields":{"eyebrow":"The pattern","headline":"Nothing about you is *broken*."}}]}

Rich text in headline-like fields: *word* becomes the Citron Instrument Serif italic word.
A final "." or "?" becomes the Citron period. Use \\n for a line break. No em dashes.
Templates and their fields: see TEMPLATES below (or README.md).
"""
import sys, os, json, html, re, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
CHROMES = [os.environ.get("CHROME_PATH",""), "/opt/google/chrome/chrome", "/opt/pw-browsers/chromium", "/usr/bin/chromium", "/usr/bin/google-chrome"]

CSS = """
@font-face{font-family:"Bricolage Grotesque";src:url("fonts/BricolageGrotesque.ttf");font-weight:200 800}
@font-face{font-family:"Space Grotesk";src:url("fonts/SpaceGrotesk.ttf");font-weight:300 700}
@font-face{font-family:"Instrument Serif";src:url("fonts/InstrumentSerif-Italic.ttf");font-style:italic}
:root{--ink:#0E1411;--ink2:#141c18;--deep:#02311F;--emerald:#046B45;--plum:#7A2E52;--citron:#C9E356;--bone:#EFEDE3;--soft:#dcdcd2;--muted:#aeb6ad;--faint:rgba(239,237,227,.12);--line:rgba(239,237,227,.09);
--card:linear-gradient(155deg,#0d4b33 0%,#02311F 78%);--cardplum:linear-gradient(155deg,#94406a 0%,#6a2747 80%);
--shadow:0 14px 34px -16px rgba(0,0,0,.75),0 2px 6px -2px rgba(0,0,0,.4);
--display:"Bricolage Grotesque",sans-serif;--body:"Space Grotesk",sans-serif;--serif:"Instrument Serif",serif}
*{box-sizing:border-box;margin:0}
body{background:#222;font-family:var(--body);color:var(--bone);-webkit-font-smoothing:antialiased}
.t{width:1080px;height:1350px;position:relative;overflow:hidden;background:var(--ink)}
.t.story{height:1920px}
.eyebrow{font-size:24px;letter-spacing:.12em;text-transform:uppercase;color:var(--citron);font-weight:600}
h1{font-family:var(--display);font-weight:800;letter-spacing:-.045em;line-height:1;font-variation-settings:"opsz" 96}
.serif{font-family:var(--serif);font-style:italic;font-weight:400;letter-spacing:0;color:var(--citron);font-size:1.08em}
.dot{color:var(--citron)}
.mark{font-family:var(--display);font-weight:800;font-size:38px;letter-spacing:-.04em}
.pill{display:inline-flex;align-items:center;gap:12px;border-radius:999px;padding:26px 44px;font:600 32px/1 var(--body)}
.pill.primary{background:var(--citron);color:var(--ink);box-shadow:0 12px 28px -12px rgba(201,227,86,.6)}
.chip{display:inline-block;border:2px solid var(--faint);background:rgba(239,237,227,.04);border-radius:999px;padding:14px 26px;font:500 28px var(--body)}
.chip.on{background:var(--emerald);border-color:var(--emerald)}
.foot{position:absolute;left:84px;right:84px;bottom:64px;display:flex;justify-content:space-between;align-items:center}
.count{font-size:26px;color:var(--muted);font-weight:500}
.pad{position:absolute;left:84px;right:84px;top:100px}
.p{font-size:38px;line-height:1.42;color:var(--soft)}
#cover h1{font-size:128px}
#cover .stack{position:absolute;left:84px;right:84px;top:330px}
#cover .card{position:absolute;left:84px;right:84px;bottom:190px;background:var(--card);border-radius:44px;padding:44px 48px;box-shadow:var(--shadow);display:flex;justify-content:space-between;align-items:center;gap:30px}
#cover .card p{font-family:var(--display);font-weight:700;font-size:40px;letter-spacing:-.03em;line-height:1.2;max-width:560px}
#body h1{font-size:92px}
#body .card{position:absolute;left:84px;right:84px;top:420px;bottom:190px;background:var(--bone);color:var(--ink);border-radius:44px;padding:56px;box-shadow:var(--shadow);display:flex;flex-direction:column;gap:26px}
#body .num{font-family:var(--display);font-weight:800;font-size:120px;letter-spacing:-.04em;color:var(--emerald);line-height:1}
#body .card .h3{font-family:var(--display);font-weight:700;font-size:54px;letter-spacing:-.03em;line-height:1.1}
#body .card .p{color:#2a2f2b;font-size:38px}
#quote-card .big{position:absolute;left:60px;right:60px;top:110px;bottom:150px;background:var(--cardplum);border-radius:64px;padding:76px 72px;box-shadow:var(--shadow);display:flex;flex-direction:column;justify-content:space-between}
#quote-card h1{font-size:132px;color:#fff;line-height:.98}
#quote-card .sig{display:flex;justify-content:space-between;align-items:center;color:#fff}
#announce .top{position:absolute;left:0;right:0;top:0;height:880px;background:var(--card);padding:100px 84px}
#announce h1{font-size:170px;margin-top:30px}
#announce .top .p{color:var(--bone);font-size:42px;margin-top:40px;max-width:820px}
#announce .strip{position:absolute;left:0;right:0;top:880px;height:150px;background:var(--citron);color:var(--ink);display:flex;align-items:center;padding:0 84px;font-family:var(--display);font-weight:700;font-size:40px;letter-spacing:-.02em}
#announce .bot{position:absolute;left:84px;right:84px;top:1090px;display:flex;flex-direction:column;gap:34px;align-items:flex-start}
#story .stack{position:absolute;left:84px;right:84px;top:520px}
#story h1{font-size:150px}
#story .chips{display:flex;flex-wrap:wrap;gap:14px;margin-top:56px}
#story .card{position:absolute;left:84px;right:84px;bottom:340px;background:var(--cardplum);border-radius:44px;padding:44px 48px;box-shadow:var(--shadow)}
#story .card p{font-family:var(--display);font-weight:700;font-size:46px;letter-spacing:-.03em;line-height:1.18;color:#fff}
#story .safe{position:absolute;left:84px;bottom:240px}
.q .wrap{position:absolute;left:84px;right:84px;top:120px;bottom:150px;display:flex;flex-direction:column;justify-content:space-between}
.q h1{font-size:136px;line-height:.98}
.q .by{display:flex;justify-content:space-between;align-items:center}
.q.plum{background:var(--plum)} .q.emerald{background:var(--emerald)} .q.bone{background:var(--bone);color:var(--ink)}
.q.bone .serif,.q.bone .dot,.q.bone .eyebrow{color:var(--emerald)}
.sign .wrap{justify-content:space-between}
.sign .mid{display:flex;flex-direction:column;gap:30px}
.sign .n{font-family:var(--serif);font-style:italic;font-size:170px;line-height:.9;color:var(--citron)}
.sign h1{font-size:88px;line-height:1.02}
.sign .p{font-size:42px;line-height:1.38;color:var(--bone);opacity:.92;max-width:900px}
.q.bone.sign .n{color:var(--emerald)} .q.bone.sign .p{color:#2a2f2b;opacity:1}
.i .wrap{position:absolute;left:84px;right:84px;top:120px;bottom:150px;display:flex;flex-direction:column}
.i.deep{background:var(--deep)}
#stat .num{font-family:var(--display);font-weight:800;font-size:380px;letter-spacing:-.06em;line-height:.9;color:var(--citron);margin-top:70px}
#stat .p{color:var(--bone);font-size:52px;line-height:1.25;font-family:var(--display);font-weight:700;letter-spacing:-.03em;margin-top:30px}
#stat .src{margin-top:auto;font-size:26px;color:var(--muted)}
#define h1{font-size:150px;margin-top:40px}
#define .pos{font-family:var(--serif);font-style:italic;font-size:54px;color:var(--citron);margin-top:18px}
#define .p{font-size:48px;line-height:1.35;color:var(--bone);margin-top:56px}
#define .ex{margin-top:auto;border-left:6px solid var(--citron);padding-left:28px;font-size:36px;color:var(--soft);line-height:1.4}
#myth .wrap{gap:28px;justify-content:center}
#myth .box{border-radius:44px;padding:52px 56px;box-shadow:var(--shadow)}
#myth .box.m{background:var(--cardplum)} #myth .box.r{background:var(--card)}
#myth .tag{font-size:24px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--citron)}
#myth h2{font-family:var(--display);font-weight:800;font-size:70px;letter-spacing:-.04em;line-height:1.04;margin-top:14px}
#list h1{font-size:96px;margin-top:26px}
#list .rows{margin-top:48px;display:flex;flex-direction:column;gap:20px}
#list .row{background:var(--ink2);border:2px solid var(--line);border-radius:36px;padding:34px 40px;display:flex;gap:30px;align-items:center}
#list .row:nth-child(1){background:var(--card);border:0}
#list .row:nth-child(3){background:var(--cardplum);border:0}
#list .n{font-family:var(--display);font-weight:800;font-size:72px;letter-spacing:-.04em;color:var(--citron);width:70px}
#list .t2{font-family:var(--display);font-weight:700;font-size:42px;letter-spacing:-.03em;line-height:1.15}
"""

def rich(s):
    s = html.escape(s or "").replace("\\n", "\n")
    s = re.sub(r"\*(.+?)\*", r'<span class="serif">\1</span>', s)
    s = re.sub(r"([.?!])\s*$", lambda m: '<span class="dot">%s</span>' % m.group(1), s)
    return s.replace("\n", "<br>")

def plain(s): return html.escape(s or "").replace("\\n", "\n").replace("\n", "<br>")
MARK = 'b<span class="dot">.</span>wylde'
def foot(f, k="tag"): return f'<div class="foot"><span class="mark">{MARK}</span><span class="count">{plain(f.get(k,""))}</span></div>'

def t_cover(f): return f'<section class="t" id="cover"><div class="pad"><div class="eyebrow">{plain(f.get("eyebrow"))}</div></div><div class="stack"><h1 data-fit="380">{rich(f.get("headline"))}</h1></div><div class="card"><p>{plain(f.get("line"))}</p><span class="pill primary">{plain(f.get("cta","Swipe →"))}</span></div>{foot(f,"counter")}</section>'
def t_body(f): return f'<section class="t" id="body"><div class="pad"><div class="eyebrow">{plain(f.get("eyebrow"))}</div><h1 style="margin-top:26px" data-fit="250">{rich(f.get("headline"))}</h1></div><div class="card"><span class="num">{plain(f.get("number"))}</span><p class="h3">{plain(f.get("title"))}</p><p class="p">{plain(f.get("text"))}</p></div>{foot(f,"counter")}</section>'
def t_quote(color):
    def fn(f):
        cls = "t q " + color if color != "ink" else "t q"
        tagstyle = ' style="color:#2a2f2b"' if color == "bone" else (' style="color:#fff;opacity:.8"' if color in ("plum","emerald") else "")
        return f'<section class="{cls}" id="quote"><div class="wrap"><div class="eyebrow">{plain(f.get("eyebrow"))}</div><h1 data-fit="860">{rich(f.get("headline"))}</h1><div class="by"><span class="mark">{MARK}</span><span class="count"{tagstyle}>{plain(f.get("tag","Save this"))}</span></div></div></section>'
    return fn
def t_quote_card(f): return f'<section class="t" id="quote-card"><div class="big"><div class="eyebrow">{plain(f.get("eyebrow"))}</div><h1 data-fit="560">{rich(f.get("headline"))}</h1><div class="sig"><span class="mark">{MARK}</span><span class="pill primary" style="padding:22px 36px;font-size:28px">{plain(f.get("tag","Save this"))}</span></div></div></section>'
def t_announce(f): return f'<section class="t" id="announce"><div class="top"><div class="eyebrow">{plain(f.get("eyebrow"))}</div><h1 data-fit="330">{rich(f.get("headline"))}</h1><p class="p">{plain(f.get("text"))}</p></div><div class="strip">{plain(f.get("strip"))}</div><div class="bot"><span class="pill primary">{plain(f.get("button","Get the free app"))}</span><span class="mark">{MARK}</span></div></section>'
def t_story(f):
    chips = "".join('<span class="chip%s">%s</span>' % (" on" if i == 0 else "", plain(c)) for i, c in enumerate(f.get("chips", [])))
    return f'<section class="t story" id="story"><div class="stack"><div class="eyebrow">{plain(f.get("eyebrow"))}</div><h1 style="margin-top:28px" data-fit="560">{rich(f.get("headline"))}</h1><div class="chips">{chips}</div></div><div class="card"><p>{plain(f.get("text"))}</p></div><div class="safe"><span class="mark">{MARK}</span></div></section>'
def t_stat(f): return f'<section class="t i deep" id="stat"><div class="wrap"><div class="eyebrow">{plain(f.get("eyebrow","Did you know"))}</div><div class="num">{plain(f.get("number"))}</div><p class="p">{plain(f.get("text"))}</p><div class="src">{plain(f.get("source"))}</div></div>{foot(f)}</section>'
def t_define(f): return f'<section class="t i" id="define"><div class="wrap"><div class="eyebrow">{plain(f.get("eyebrow","Word of the day"))}</div><h1>{rich(f.get("term"))}</h1><div class="pos">{plain(f.get("pos"))}</div><p class="p">{plain(f.get("text"))}</p><div class="ex">{plain(f.get("example"))}</div></div>{foot(f)}</section>'
def t_myth(f): return f'<section class="t i" id="myth"><div class="wrap"><div class="box m"><div class="tag">Myth</div><h2 data-fit="330">{rich(f.get("myth"))}</h2></div><div class="box r"><div class="tag">Reality</div><h2 data-fit="330">{rich(f.get("reality"))}</h2></div></div>{foot(f)}</section>'
def t_list(f):
    rows = "".join(f'<div class="row"><span class="n">{i+1}</span><span class="t2">{plain(x)}</span></div>' for i, x in enumerate(f.get("items", [])[:3]))
    return f'<section class="t i" id="list"><div class="wrap"><div class="eyebrow">{plain(f.get("eyebrow","Three things"))}</div><h1 data-fit="300">{rich(f.get("headline"))}</h1><div class="rows">{rows}</div></div>{foot(f)}</section>'

def t_sign(color):
    def fn(f):
        cls = "t q sign " + color if color != "ink" else "t q sign"
        tagstyle = ' style="color:#2a2f2b"' if color == "bone" else (' style="color:#fff;opacity:.8"' if color in ("plum","emerald") else "")
        return f'<section class="{cls}" id="sign"><div class="wrap"><div class="eyebrow">{plain(f.get("eyebrow"))}</div><div class="mid"><div class="n">{plain(f.get("number"))}</div><h1 data-fit="330">{rich(f.get("headline"))}</h1><p class="p">{plain(f.get("text"))}</p></div><div class="by"><span class="mark">{MARK}</span><span class="count"{tagstyle}>{plain(f.get("tag","Swipe →"))}</span></div></div></section>'
    return fn

TEMPLATES = {
  "cover": (t_cover, 1350), "body": (t_body, 1350),
  "quote-ink": (t_quote("ink"), 1350), "quote-plum": (t_quote("plum"), 1350),
  "quote-emerald": (t_quote("emerald"), 1350), "quote-bone": (t_quote("bone"), 1350),
  "sign-ink": (t_sign("ink"), 1350), "sign-plum": (t_sign("plum"), 1350),
  "sign-emerald": (t_sign("emerald"), 1350), "sign-bone": (t_sign("bone"), 1350),
  "quote-card": (t_quote_card, 1350), "announce": (t_announce, 1350), "story": (t_story, 1920),
  "stat": (t_stat, 1350), "define": (t_define, 1350), "myth": (t_myth, 1350), "list": (t_list, 1350),
}

FIT_JS = """() => { // shrink any [data-fit] heading until it fits its max height (px)
  const out=[];
  document.querySelectorAll('[data-fit]').forEach(el=>{const max=+el.dataset.fit;let fs=parseFloat(getComputedStyle(el).fontSize);
    while(el.getBoundingClientRect().height>max && fs>40){fs-=4;el.style.fontSize=fs+'px';}
    out.push(Math.round(fs));});
  return out;}"""

def find_chrome():
    for c in CHROMES:
        if c and os.path.exists(c): return c
    return None

def main():
    from playwright.sync_api import sync_playwright
    from PIL import Image
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    work = tempfile.mkdtemp(dir=HERE)  # keeps relative font paths working
    shutil.copytree(os.path.join(HERE, "fonts"), os.path.join(work, "fonts"))
    results = []
    with sync_playwright() as p:
        exe = find_chrome()
        b = p.chromium.launch(executable_path=exe, args=["--allow-file-access-from-files"]) if exe else p.chromium.launch(args=["--allow-file-access-from-files"])
        for i, s in enumerate(spec["slides"], 1):
            fn, h = TEMPLATES[s["template"]]
            for bad in ("—", "–"):
                for v in json.dumps(s.get("fields", {}), ensure_ascii=False).split('"'):
                    if bad in v: raise SystemExit(f"Slide {i}: remove em/en dashes from copy: {v!r}")
            page_html = f"<!doctype html><meta charset=utf-8><style>{CSS}</style>{fn(s.get('fields', {}))}"
            hp = os.path.join(work, f"s{i}.html"); open(hp, "w").write(page_html)
            pg = b.new_page(viewport={"width": 1080, "height": h}, device_scale_factor=1)
            pg.goto(f"file://{hp}"); pg.wait_for_timeout(900); pg.evaluate("document.fonts.ready")
            sizes = pg.evaluate(FIT_JS)
            png = os.path.join(out, f"slide-{i}.png"); pg.locator("section").screenshot(path=png)
            jpg = os.path.join(out, f"slide-{i}.jpg"); Image.open(png).convert("RGB").save(jpg, "JPEG", quality=93)
            os.remove(png); pg.close(); results.append((jpg, sizes))
        b.close()
    shutil.rmtree(work)
    for j, sz in results: print(j, "headline sizes:", sz)

if __name__ == "__main__": main()
