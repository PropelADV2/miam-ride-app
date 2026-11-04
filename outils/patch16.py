t=open('build_osm15.py').read()
t=t.replace("Miam ride osm - vers 15.html","Miam ride osm - vers 16.html")
# 1) GEO + champ d'arrivée réécrits
a=t.index("const GEO={cache:{},"); b=t.index("{const b0=baseKm;")
new=r"""const GEO={cache:{},fail:false,async search(q,n){const c=gStart(),out=[],add=r=>{if(r&&r.label&&!out.some(o=>o.label===r.label))out.push(r)};let ok=0;
 const ph=fetchT('https://photon.komoot.io/api/?limit='+(n||1)+'&lang=fr&lat='+c.lat+'&lon='+c.lng+'&q='+encodeURIComponent(q),{},7000).then(async r=>{if(!r.ok)throw 0;ok++;return((await r.json()).features||[]).map(F=>{const p=F.properties;return{lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:[p.name,p.street&&((p.housenumber?p.housenumber+' ':'')+p.street),[p.postcode,p.city||p.county].filter(Boolean).join(' ')].filter(Boolean).join(', ')}})}).catch(()=>[]);
 const ba=fetchT('https://api-adresse.data.gouv.fr/search/?limit='+(n||1)+'&lat='+c.lat+'&lon='+c.lng+'&q='+encodeURIComponent(q),{},7000).then(async r=>{if(!r.ok)throw 0;ok++;return((await r.json()).features||[]).map(F=>({lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:F.properties.label}))}).catch(()=>[]);
 const [P,B]=await Promise.all([ph,ba]);this.fail=!ok;
 const addr=/^\d|\b(rue|avenue|av\.?|boulevard|bd|chemin|route|impasse|all[eé]e|place|quai)\b/i.test(q);(addr?[B,P]:[P,B]).forEach(L=>L.forEach(add));return out.slice(0,n||1)}};
function destSet(g){const t=$('#to');S.dest={lat:g.lat,lng:g.lng,label:g.label};S.destKm=0;if(t)t.value=g.label;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;OSMC.key=null;OSMC.k2=null;try{showRes()}catch(e){}try{drawMap(true)}catch(e){}osmToast('Arrivée : '+g.label)}
let _dp=null;async function destResolve(){const t=$('#to'),v=t?t.value.trim():'';if(S.dest&&S.dest.label===v)return S.dest;if(v.length<3)return null;if(_dp)return _dp;
 _dp=(async()=>{try{const g=(await GEO.search(v,1))[0];if(g)destSet(g);else{S.dest=null;osmToast(GEO.fail?'Recherche d’adresse indisponible (connexion). Réessaie dans un instant.':'Lieu introuvable : précise la ville ou le nom complet')}return S.dest}finally{_dp=null}})();return _dp}
(()=>{const t=$('#to');if(!t)return;t.setAttribute('autocomplete','off');const row=$('#toRow');if(!row)return;
 const box=document.createElement('div');box.id='to_box';box.hidden=true;box.setAttribute('role','listbox');box.style.cssText='position:absolute;left:0;right:0;top:100%;z-index:60;background:#fff;border:2px solid var(--ink);border-radius:14px;margin-top:4px;box-shadow:0 8px 24px rgba(0,0,0,.18);overflow:hidden';
 row.style.position='relative';row.appendChild(box);box.addEventListener('mousedown',e=>e.preventDefault());
 const show=(L,msg)=>{box.innerHTML='';if(msg){const p=document.createElement('div');p.textContent=msg;p.style.cssText='padding:10px 12px;font:600 13px Poppins,sans-serif;color:var(--muted)';box.appendChild(p)}
  L.forEach(g=>{const b=document.createElement('button');b.type='button';b.setAttribute('role','option');b.textContent=g.label;b.style.cssText='display:block;width:100%;text-align:left;border:0;border-top:1px solid #eee;background:#fff;padding:10px 12px;font:600 13px Poppins,sans-serif;cursor:pointer';b.onclick=()=>{box.hidden=true;destSet(g)};box.appendChild(b)});box.hidden=false};
 let tm,seq=0;t.addEventListener('input',()=>{clearTimeout(tm);const v=t.value.trim();if(S.dest&&S.dest.label!==v)S.dest=null;if(v.length<3){box.hidden=true;return}
  tm=setTimeout(async()=>{const my=++seq;show([],'Recherche…');const R=await GEO.search(v,5);if(my!==seq)return;show(R,R.length?'':(GEO.fail?'Recherche indisponible (connexion). Réessaie.':'Aucun résultat : précise la ville'))},300)});
 t.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();clearTimeout(tm);seq++;box.hidden=true;destResolve()}});
 t.addEventListener('change',()=>{clearTimeout(tm);seq++;box.hidden=true;destResolve()});
 document.addEventListener('click',e=>{if(!row.contains(e.target))box.hidden=true})})();
"""
t=t[:a]+new+t[b:]
# 2) osmDest attend la résolution du lieu tapé
x="async function osmDest(c,km,bearing){const D=S.dest;\n if(!D)throw usrErr('Choisis d’abord un lieu d’arrivée dans le champ « Lieu d’arrivée »');"
assert x in t
t=t.replace(x,"async function osmDest(c,km,bearing){const D=S.dest||await destResolve();\n if(!D)throw usrErr(($('#to')&&$('#to').value.trim().length>=3)?'Lieu d’arrivée introuvable : précise la ville ou choisis une suggestion':'Choisis d’abord un lieu d’arrivée dans le champ « Lieu d’arrivée »');")
open('build_osm16.py','w').write(t)
