"""Battle cards on an iPhone-Duo style foldable.
Left screen = the card front (What / Why / How).  Right screen = the visual (a rich illustration + title pill + caption + chips).
Transparent outside the device so it works on light and dark pages.

usage: python3 duo.py spec.json outdir
spec.json = [{"id":"001","front":"/path/front.png","art":"/path/art.jpg","emoji":"🏭","title":"The content factory",
              "caption":"Warehouse for the brand, factory for content","chips":["🧠 memory","🏭 make ×100","👀 pick 3"]}, ...]
"""
import sys, json, base64, pathlib, asyncio, subprocess, html as H
from playwright.async_api import async_playwright

R = pathlib.Path(__file__).parent
FONT = base64.b64encode((R / 'AlloVariable.woff2').read_bytes()).decode()
SW, SH = 620, 1240          # one screen, CSS px (rendered at 2x)

def uri(p):
    p = pathlib.Path(p); ext = 'png' if p.suffix == '.png' else 'jpeg'
    return f'data:image/{ext};base64,' + base64.b64encode(p.read_bytes()).decode()

def right_screen(s):
    chips = ''.join(f'<span class="chip">{H.escape(c)}</span>' for c in s.get('chips', []))
    return f'''<div class="rs">
  <div class="pill">{s.get('emoji','')} {H.escape(s['title'])}</div>
  <div class="art"><img src="{uri(s['art'])}"></div>
  <div class="cap">{H.escape(s['caption'])}</div>
  <div class="chips">{chips}</div>
</div>'''

CSS = f'''@font-face{{font-family:Allo;src:url(data:font/woff2;base64,{FONT})}}
*{{margin:0;padding:0;box-sizing:border-box;font-family:Allo,sans-serif;font-variation-settings:'ROND' 100}}
html,body{{background:transparent}}
.stage{{width:{2*SW+220}px;height:{SH+150}px;display:flex;align-items:center;justify-content:center;perspective:3200px}}
.dev{{display:flex;transform-style:preserve-3d}}
.half{{width:{SW+18}px;height:{SH+36}px;background:#1d1d1f;padding:18px;position:relative;
  box-shadow:0 0 0 5px #b9b9be, 0 0 0 7px #6e6e73, inset 0 0 0 2px #8e8e93}}
.half.l{{border-radius:78px 0 0 78px;padding-right:0;transform-origin:right center;transform:rotateY(13deg)}}
.half.r{{border-radius:0 78px 78px 0;padding-left:0;transform-origin:left center;transform:rotateY(-13deg)}}
.scr{{width:{SW}px;height:{SH}px;overflow:hidden;background:#fff;position:relative}}
.l .scr{{border-radius:62px 0 0 62px}} .r .scr{{border-radius:0 62px 62px 0}}
.l .scr::after,.r .scr::after{{content:'';position:absolute;top:0;bottom:0;width:46px;pointer-events:none}}
.l .scr::after{{right:0;background:linear-gradient(90deg,rgba(0,0,0,0),rgba(0,0,0,.10))}}
.r .scr::after{{left:0;background:linear-gradient(270deg,rgba(0,0,0,0),rgba(0,0,0,.07))}}
.front{{width:100%;display:block}}
.status{{position:absolute;top:22px;font-size:20px;font-weight:800;color:#1d1d1f;z-index:3}}
.l .status{{left:56px}} .r .status{{right:56px}}
.cam{{position:absolute;top:22px;right:120px;width:26px;height:26px;border-radius:50%;background:#111;z-index:3;box-shadow:0 0 0 3px #e5e5ea}}
.rs{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;padding:74px 34px 40px;gap:22px}}
.pill{{background:#d9f0ff;color:#1f7fe8;font-weight:900;font-size:27px;text-transform:uppercase;letter-spacing:.02em;padding:8px 20px;border-radius:16px;white-space:nowrap;max-width:100%;overflow:hidden;text-overflow:ellipsis}}
.art{{flex:1;width:100%;border-radius:40px;overflow:hidden;background:#f2f2f4}}
.art img{{width:100%;height:100%;object-fit:cover;display:block}}
.cap{{word-spacing:.12em;font-size:31px;font-weight:900;line-height:1.15;color:#2b2b2e;text-align:center;padding:0 6px}}
.chips{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}}
.chip{{background:#f2f2f4;color:#3a3a3a;font-weight:800;font-size:21px;padding:9px 16px;border-radius:999px;white-space:nowrap}}
.hinge{{position:absolute;left:50%;top:{75}px;width:10px;height:{SH+36}px;margin-left:-5px;background:linear-gradient(90deg,#0c0c0d,#3a3a3c,#0c0c0d);transform:translateZ(-1px)}}
'''

def page(s):
    front = f'<img class="front" src="{uri(s["front"])}">'
    return f'''<html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class="stage"><div class="dev">
<div class="half l"><div class="scr"><div class="status">9:41</div>{front}</div></div>
<div class="half r"><div class="scr"><span class="cam"></span>{right_screen(s)}</div></div>
</div></div></body></html>'''

async def main(spec, out):
    out = pathlib.Path(out).resolve(); out.mkdir(parents=True, exist_ok=True)
    tmp = out / '_html'; tmp.mkdir(exist_ok=True)
    files = []
    for s in spec:
        f = tmp / f'{s["id"]}.html'; f.write_text(page(s)); files.append(f)
    subprocess.run(['python3', str(R / 'apple_emoji.py')] + [str(f) for f in files], cwd=str(R), check=True, stdout=subprocess.DEVNULL)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 2 * SW + 220, 'height': SH + 150}, device_scale_factor=1)
        for s, f in zip(spec, files):
            await pg.goto('file://' + str(f)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.locator('.stage').screenshot(path=str(out / f'{s["id"]}.png'), omit_background=True)
            print('ok', s['id'])
        await b.close()

if __name__ == '__main__':
    asyncio.run(main(json.load(open(sys.argv[1])), sys.argv[2]))
