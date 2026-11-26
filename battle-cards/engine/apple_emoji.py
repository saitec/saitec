"""Swap every emoji in slide HTML for an inline Apple emoji image.
usage: python3 tools/apple_emoji.py build/*.html   (rewrites in place, caches PNGs in ./emoji/)
"""
import base64, json, pathlib, re, sys, urllib.request

CACHE = pathlib.Path("emoji"); CACHE.mkdir(exist_ok=True)
NAMES = "https://cdn.jsdelivr.net/npm/unicode-emoji-json@0.9.0/data-by-emoji.json"
BIG = "https://em-content.zobj.net/source/apple/{v}/{slug}_{cp}.png"          # 160px
SMALL = "https://cdn.jsdelivr.net/npm/emoji-datasource-apple@16.0.0/img/apple/64/{cp}.png"
VERSIONS = [419, 391, 354]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read() if r.status == 200 else None

names = json.loads(get(NAMES))
TONES = {0x1F3FB: "light", 0x1F3FC: "medium-light", 0x1F3FD: "medium",
         0x1F3FE: "medium-dark", 0x1F3FF: "dark"}
# longest first so ZWJ / flag sequences match whole; skin tones ride along
UNIT = "(?:" + "|".join(re.escape(e) for e in sorted(names, key=len, reverse=True)) + ")[\U0001F3FB-\U0001F3FF]?"
EMOJI = re.compile(f"{UNIT}(?:{UNIT})*")

def png(e):
    cp = "-".join(f"{ord(c):x}" for c in e)
    f = CACHE / f"{cp}.png"
    if f.exists():
        return f.read_bytes()
    tones = [TONES[ord(c)] for c in e if ord(c) in TONES]
    base = "".join(c for c in e if ord(c) not in TONES)
    tries = []
    if base in names and len(tones) <= 1:
        slug = names[base]["slug"].replace("_", "-")
        if tones:
            slug += f"-{tones[0]}-skin-tone"
        tries = [BIG.format(v=v, slug=slug, cp=cp) for v in VERSIONS]
    padded = "-".join(f"{ord(c):04x}" for c in e)
    bare = "-".join(f"{ord(c):04x}" for c in e if ord(c) != 0xFE0F)
    tries += [SMALL.format(cp=padded), SMALL.format(cp=bare)]
    for u in tries:
        try:
            data = get(u)
            if data:
                if u.startswith(SMALL[:40]):
                    print(f"  {e} only exists at 64px: fine inline, swap it in big icon circles")
                f.write_bytes(data); return data
        except Exception:
            pass
    sys.exit(f"no Apple image for {e} ({cp}); swap it for another emoji")

def img(m):
    e = m.group(0)
    b64 = base64.b64encode(png(e)).decode()
    return (f'<img class="ae" alt="{e}" src="data:image/png;base64,{b64}" '
            f'style="height:1em;width:1em;vertical-align:-0.12em;display:inline-block">')

TAG = re.compile(r"(<[^>]*>)")  # never touch emoji inside tags/attributes
for path in sys.argv[1:]:
    p = pathlib.Path(path)
    parts = TAG.split(p.read_text())
    out = "".join(s if s.startswith("<") else EMOJI.sub(img, s) for s in parts)
    p.write_text(out)
    print(p, "ok")
