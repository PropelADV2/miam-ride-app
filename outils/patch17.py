t=open('build_osm16.py').read()
def rp(a,b):
    global t
    assert t.count(a)==1,(a[:80],t.count(a)); t=t.replace(a,b)
t=t.replace("Miam ride osm - vers 16.html","Miam ride osm - vers 17.html")
# ancien gestionnaire du champ de départ neutralisé
rp("f.addEventListener('change',async()=>{const v=f.value.trim();if(!osmOn()||v.length<3||/^ma position$/i.test(v))return;f.disabled=true;","f.addEventListener('change',async()=>{return;const v=f.value.trim();f.disabled=true;")
rp("osmToast('Départ : '+f.value);osmWarm()},","S.fromLabel=f.value;osmToast('Départ : '+f.value);osmWarm()},")
# suggestions pour le départ
code=r"""/* ---------- départ : suggestions d'adresses (comme l'arrivée) ---------- */
function startSet(g){const f=$('#from');C0=[g.lng,g.lat];S.fromLabel=g.label;if(f)f.value=g.label;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;S.osmEarly=null;OSMC.key=null;OSMC.k2=null;try{showRes()}catch(e){}try{drawMap(true)}catch(e){}osmWarm();osmToast('Départ : '+g.label)}
let _sp=null;async function startResolve(){const f=$('#from'),v=f?f.value.trim():'';if(v.length<3||/^ma position$/i.test(v)||v===S.fromLabel)return;if(_sp)return _sp;
 _sp=(async()=>{try{const g=(await GEO.search(v,1))[0];if(g)startSet(g);else osmToast(GEO.fail?'Recherche d’adresse indisponible (connexion). Réessaie dans un instant.':'Adresse de départ introuvable : précise la ville')}finally{_sp=null}})();return _sp}
(()=>{const f=$('#from');if(!f)return;S.fromLabel=f.value.trim();f.setAttribute('autocomplete','off');const row=f.closest('label')||f.parentNode;
 const box=document.createElement('div');box.id='from_box';box.hidden=true;box.setAttribute('role','listbox');box.style.cssText='position:absolute;left:0;right:0;top:100%;z-index:60;background:#fff;border:2px solid var(--ink);border-radius:14px;margin-top:4px;box-shadow:0 8px 24px rgba(0,0,0,.18);overflow:hidden';
 row.style.position='relative';row.appendChild(box);box.addEventListener('mousedown',e=>e.preventDefault());
 const show=(L,msg)=>{box.innerHTML='';if(msg){const p=document.createElement('div');p.textContent=msg;p.style.cssText='padding:10px 12px;font:600 13px Poppins,sans-serif;color:var(--muted)';box.appendChild(p)}
  L.forEach(g=>{const b=document.createElement('button');b.type='button';b.setAttribute('role','option');b.textContent=g.label;b.style.cssText='display:block;width:100%;text-align:left;border:0;border-top:1px solid #eee;background:#fff;padding:10px 12px;font:600 13px Poppins,sans-serif;cursor:pointer';b.onclick=()=>{box.hidden=true;startSet(g)};box.appendChild(b)});box.hidden=false};
 let tm,seq=0;f.addEventListener('input',()=>{clearTimeout(tm);const v=f.value.trim();if(v.length<3||/^ma position$/i.test(v)){box.hidden=true;return}
  tm=setTimeout(async()=>{const my=++seq;show([],'Recherche…');const R=await GEO.search(v,5);if(my!==seq)return;show(R,R.length?'':(GEO.fail?'Recherche indisponible (connexion). Réessaie.':'Aucun résultat : précise la ville'))},300)});
 f.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();clearTimeout(tm);seq++;box.hidden=true;startResolve()}});
 f.addEventListener('change',()=>{clearTimeout(tm);seq++;box.hidden=true;startResolve()});
 document.addEventListener('click',e=>{if(!row.contains(e.target))box.hidden=true})})();
{const g2=gPrepare;gPrepare=async function(){if(osmOn())try{await startResolve()}catch(e){}return g2.apply(this,arguments)}}
"""
rp("/* ---------- validation des boulangeries (Profil › Compte) ---------- */",code+"/* ---------- validation des boulangeries (Profil › Compte) ---------- */")
# preuve visible que le lieu d'arrivée est pris en compte
rp("q.textContent=R.amb?","""let z=document.getElementById('osm_dest');if(!z){z=document.createElement('p');z.id='osm_dest';z.className='sub';z.style.cssText='font-size:12px;margin:0 0 6px;font-weight:600';q.after(z)}
 z.textContent='';if(S.mode==='dest'&&S.dest&&R.path&&R.path.length>1){let best=1e9,at=0,acc=0,tot=0;const cum=[0];for(let i=1;i<R.path.length;i++){acc+=hav(R.path[i-1],R.path[i]);cum.push(acc)}tot=acc;R.path.forEach((p,i)=>{const dd=hav(p,S.dest);if(dd<best){best=dd;at=cum[i]}});
  z.textContent=best<=0.3?(S.fast?'Arrivée : ':'Passage par : ')+S.dest.label+(S.fast?'':' · au km '+Math.round(at)):'Attention : le tracé passe à '+(best<1?Math.round(best*1000)+' m':best.toFixed(1)+' km')+' de '+S.dest.label}
 q.textContent=R.amb?""")
open('build_osm17.py','w').write(t)
