// usage: node render.js cards/cards_01.js out/01   -> writes out/01/index.html, PNGs, report.json
const fs=require('fs'), path=require('path');
const { chromium } = require('playwright');
const [,, cardsFile, outDir] = process.argv;
const cards = require(path.resolve(cardsFile));
fs.mkdirSync(outDir,{recursive:true});
const {buildHtml}=require('./build');
const html = buildHtml(cards);
fs.writeFileSync(path.join(outDir,'index.html'),html);
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1480,height:1500},deviceScaleFactor:2});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+path.resolve(outDir,'index.html'));
  await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(5000);
  const report = await p.$$eval('.card', els=>els.map(e=>{
    const num=e.dataset.num, kind=e.classList.contains('front')?'front':'back';
    const foot=e.querySelector('.foot').getBoundingClientRect();
    const r={num,kind,issues:[]};
    if(kind==='front'){
      const cb=e.getBoundingClientRect(); const bands=[...e.querySelectorAll('.band')]; const last=bands[bands.length-1].getBoundingClientRect();
      r.slack=Math.round((cb.bottom-34)-foot.bottom); if(r.slack<0) r.issues.push('front overflow by '+(-r.slack)+'px (footer pushed out of the card)');
      r.slack=Math.round(foot.top-last.bottom)+Math.min(0,Math.round((cb.bottom-34)-foot.bottom));
      if(r.slack>220) r.issues.push('front has '+r.slack+'px empty space, consider a takeaway band or one more line');
      const h1e=e.querySelector('h1'); const h1=h1e?h1e.getBoundingClientRect():{height:0}; if(h1.height>120) r.issues.push('title wraps to 3 lines');
    } else {
      const svg=e.querySelector('svg.art'); const sb=svg.getBoundingClientRect();
      r.slack=Math.round(foot.top-sb.bottom);
      const scale=sb.width/541;
      for(const t of svg.querySelectorAll('text')){ if((t.getAttribute('transform')||'').includes('rotate')) continue; const bb=t.getBBox(); const x1=bb.x, x2=bb.x+bb.width, y2=bb.y+bb.height;
        if(x1<4||x2>537||y2>1118||bb.y<0) r.issues.push(`text "${(t.textContent||'').slice(0,28)}" out of bounds (x ${Math.round(x1)}..${Math.round(x2)}, y ${Math.round(bb.y)}..${Math.round(y2)})`); }
      const n=svg.querySelectorAll('text,rect,circle,path,polygon').length; if(n<12) r.issues.push('back looks thin ('+n+' elements)');
      const caption=[...svg.querySelectorAll('text')].find(t=>+t.getAttribute('y')>=1050); if(!caption) r.issues.push('no bottom caption near y=1070');
    }
    return r; }));
  const cardsEls=await p.$$('.card');
  for(let i=0;i<cardsEls.length;i++){ const r=report[i]; await cardsEls[i].screenshot({path:path.join(outDir,`${String(r.num).padStart(3,'0')}-${r.kind}.png`)}); }
  fs.writeFileSync(path.join(outDir,'report.json'),JSON.stringify({errs,report},null,1));
  const bad=report.filter(r=>r.issues.length);
  console.log(`${cards.length} cards rendered to ${outDir}. page errors: ${errs.length}`);
  for(const r of bad) console.log(`#${r.num} ${r.kind}: `+r.issues.join(' | '));
  if(!bad.length) console.log('no layout issues');
  await b.close();
})();
