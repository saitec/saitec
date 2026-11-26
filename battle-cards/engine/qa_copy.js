const path=require('path');
const files=process.argv.slice(2);
for(const f of files){const cards=require(path.resolve(f));
for(const c of cards){
  const heads=[c.title,...c.bands.map(b=>b.headline)];
  const all=[...heads,...c.bands.flatMap(b=>b.body)].join(' | ');
  const iss=[];
  if(/—/.test(all+c.svg)) iss.push('em dash');
  heads.forEach(h=>{ if(/\b(don'?t|isn'?t|dont|isnt)\b/i.test(h)) iss.push('neg head: '+h);
    if(/\bnot\b[^.]*,\s*(it'?s|but)\b/i.test(h)) iss.push('notX: '+h);});
  if(/\b(actually|in reality|in fact)\b/i.test(all)) iss.push('banned word');
  if(iss.length) console.log(c.num, c.title, '::', iss.join(' ; '));
}}
