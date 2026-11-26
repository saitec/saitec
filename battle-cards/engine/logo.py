import base64,asyncio,subprocess,pathlib
from playwright.async_api import async_playwright
B=base64.b64encode(open('/home/claude/bd/AlloVariable.woff2','rb').read()).decode()
css=f"<meta charset='utf-8'><style>@font-face{{font-family:Allo;src:url(data:font/woff2;base64,{B})}}*{{margin:0;font-family:Allo;font-variation-settings:'ROND' 100}}html,body{{background:transparent}}</style>"
logo='<section id="logo" style="width:600px;height:600px;display:flex;align-items:center;justify-content:center"><div style="width:560px;height:560px;border-radius:50%;background:#F4C842;border:14px solid #2F2F2F;display:flex;align-items:center;justify-content:center;font-size:300px">⚔️</div></section>'
word='<section id="word" style="width:1600px;height:400px;display:flex;align-items:center;justify-content:center"><div style="display:flex;align-items:center;gap:36px;background:#FDFDFB;border:10px solid #2F2F2F;border-radius:200px;padding:30px 80px 30px 34px"><div style="width:260px;height:260px;border-radius:50%;background:#F4C842;border:10px solid #2F2F2F;display:flex;align-items:center;justify-content:center;font-size:140px">⚔️</div><div style="font-size:170px;font-weight:900;color:#2F2F2F;white-space:nowrap">Battle Cards</div></div></section>'
for n,h in [('logo',logo),('word',word)]: pathlib.Path(n+'.html').write_text(css+h)
subprocess.run(['python3','/home/claude/bd/tools/apple_emoji.py','/home/claude/brand/logo.html','/home/claude/brand/word.html'],cwd='/home/claude/bd',check=True,stdout=subprocess.DEVNULL)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1700,'height':700})
    for n in ['logo','word']:
      await pg.goto('file:///home/claude/brand/'+n+'.html');await pg.evaluate('document.fonts.ready');await pg.wait_for_timeout(300)
      await pg.locator('section').screenshot(path=f'/home/claude/brand/{n}.png',omit_background=True)
    await b.close()
asyncio.run(m())
