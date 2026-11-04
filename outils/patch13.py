t=open('build_osm.py').read()
def rp(a,b):
    global t
    assert t.count(a)==1,(a[:80],t.count(a)); t=t.replace(a,b)
t=t.replace("open('/mnt/user-data/outputs/Miam ride osm - vers 12.html','w')","open('/mnt/user-data/outputs/Miam ride osm - vers 13.html','w')")
assert 'vers 13' in t
# libellé de statut à la place de « pas encore noté »
rp("b[4]?`${b[3].toFixed(1).replace('.',',')}/5, ${b[4]} avis`:'pas encore noté';\")","b[4]?`${b[3].toFixed(1).replace('.',',')}/5, ${b[4]} avis`:(typeof bLabel==='function'?bLabel(b):'pas encore noté');\")")
# filtre chaînes / grandes surfaces
rp("function osmClean(L){const out=[];for(const p of L){if(!p||p.name==='Boulangerie')continue;",
   "function osmClean(L){const out=[];for(const p of L){if(!p||p.name==='Boulangerie'||(typeof OSMR!=='undefined'&&OSMR.chains.test(p.name)))continue;")
rp("if(z){return z.l.map(x=>({id:x[0],name:x[1],addr:x[2],lat:x[3],lng:x[4],rating:0,reviews:0,hours:x[6]?osmHours(x[6]):null}))}",
   "if(z){return osmClean(z.l.map(x=>({id:x[0],name:x[1],addr:x[2],lat:x[3],lng:x[4],rating:0,reviews:0,hours:x[6]?osmHours(x[6]):null})))}")
# règles + statuts + évaluation des pauses (insérés avant le bloc ambiance)
blk=r"""/* ---------- règles boulangeries (réglables ici) ---------- */
const OSMR={denseN:12,       // nb de boulangeries dans la zone à partir duquel on est en « ville »
 minValid:4,                 // en ville : nb mini de boulangeries validées/notées pour ne proposer qu'elles
 minRev:5,minNote:3.5,       // avis cyclistes (QR) : nb mini d'avis, note mini (en dessous : écartée)
 budgetCamp:1.5,             // campagne : budget de détour multiplié par ce facteur
 wVille:6,wCamp:10,          // poids des boulangeries dans le choix de la boucle
 failPen:1000,fewPen:8,      // pause sans aucune boulangerie ouverte / avec moins de 2 choix
 chains:/^(?:boulangerie\s+)?(?:paul|ange|marie blach[eè]re|la mie c[aâ]line|brioche dor[eé]e|carrefour|leclerc|auchan|lidl|intermarch[eé]|monoprix|franprix|casino|super u|u express|picard|aldi|cora|g20|simply)(?:\s+(?:market|city|contact|express|bio))?(?:\s*[-–,(].*)?$/i};
const BST={c:null,get(){if(!this.c){try{this.c=JSON.parse(OSMS.get('mr_bstat')||'{}')}catch(e){this.c={}}}return this.c},set(id,s,n){const o=this.get();if(s==='n')delete o[id];else o[id]={s,n:n||''};OSMS.set('mr_bstat',JSON.stringify(o))}};
/* statuts : v validée par nous · r notée par les cyclistes · n non vérifiée · x à éviter (écartée) */
function bStat(p){const v=BST.get()[p.id];if(v&&v.s)return v.s;if((p.reviews||0)>=OSMR.minRev)return p.rating>=OSMR.minNote?'r':'x';return'n'}
const bStatT=b=>bStat({id:b[9]&&b[9].id,rating:b[3],reviews:b[4]});
function bLabel(b){const s=bStatT(b);return s==='v'?'Validée par Miam Ride':s==='r'?'Notée par les cyclistes':'Pas encore vérifiée'}
function bkEval(h,P,mode){const np=S.np,W=RULES.win[np];if(!np||!W||isDetour()||!h.path||!h.path.length)return{pen:0,n:[],cnt:[],none:false};
 const cum=[0];for(let i=1;i<h.path.length;i++)cum.push(cum[i-1]+hav(h.path[i-1],h.path[i]));const T=cum[cum.length-1]||1,bud=RULES.budget[np]*(mode==='campagne'?OSMR.budgetCamp:1),ns=[],cn=[];let pen=0,none=false;
 W.forEach(([lo,hi],j)=>{const pts=[];for(let i=0;i<h.path.length;i+=6){const f=cum[i]/T;if(f>=lo&&f<=hi)pts.push(h.path[i])}
  let sc=0,k=0;for(const p of P){let dm=1e9;for(const q of pts){const d=hav(p,q);if(d<dm)dm=d}
   if(dm*2*1.3>bud)continue;let st='open';try{st=hState(gTuple(p,h.path),j,Math.round(h.km))}catch(e){}if(st==='closed')continue;
   k++;sc+=(p.hours?1:.5)*(bStat(p)==='v'?1.5:1)}
  ns.push(Math.round(sc*10)/10);cn.push(k);
  if(sc===0){none=true;pen+=OSMR.failPen}else{pen-=Math.min(sc,4)*(mode==='campagne'?OSMR.wCamp:OSMR.wVille);if(sc<2)pen+=OSMR.fewPen}});
 return{pen,n:ns,cnt:cn,none}}
{const z0=zoneApply;zoneApply=function(tu){if(osmOn()){tu=tu.filter(b=>bStatT(b)!=='x');if(OSMC.strict){const v=tu.filter(b=>{const s=bStatT(b);return s==='v'||s==='r'});if(v.length)tu=v}}return z0.call(this,tu)}}
"""
rp("/* ---------- ambiance : plusieurs boucles candidates",blk+"/* ---------- ambiance : plusieurs boucles candidates")
rp("return dev*a.wd+Math.max(0,a.calm-cm)*a.wk-Math.max(0,cm-a.calm)*a.we+(r.busy||0)*a.wb+(r.unpaved||0)*1.5}",
   "const f=r.bk&&r.bk.mode==='campagne'?.6:1;return dev*a.wd+f*(Math.max(0,a.calm-cm)*a.wk-Math.max(0,cm-a.calm)*a.we+(r.busy||0)*a.wb)+(r.unpaved||0)*1.5+(r.pen||0)}")
rp(" let best=null;\n if(out.length){out.sort(",
""" let L0=null;try{const pr=OSMC.pre&&OSMC.pre.p;if(pr)L0=await Promise.race([pr,new Promise(r=>setTimeout(()=>r(null),20000))])}catch(e){}
 let P0=null,mode='ville';OSMC.strict=false;
 if(Array.isArray(L0)){P0=L0.filter(p=>bStat(p)!=='x');const dn=P0.filter(p=>hav(p,c)<=rU*1.4).length;mode=dn>=OSMR.denseN?'ville':'campagne';OSMC.mode=mode;
  if(mode==='ville'){const V=P0.filter(p=>{const s=bStat(p);return s==='v'||s==='r'});if(V.length>=OSMR.minValid){P0=V;OSMC.strict=true}}}
 const bk=h=>{const e=P0?bkEval(h,P0,mode):{pen:0,n:[],cnt:[],none:false};h.pen=e.pen;h.bk={n:e.n,cnt:e.cnt,none:e.none,mode,strict:OSMC.strict,known:!!P0}};
 out.forEach(bk);
 let best=null;
 if(out.length){out.sort(""")
rp("if(h&&ambScore(h,km)<ambScore(best,km)){out.push(h);best=h}","if(h)bk(h);if(h&&ambScore(h,km)<ambScore(best,km)){out.push(h);best=h}")
# affichage
a=t.index("q.textContent=R.amb?"); b=t.index("\n",a)
newq=r"""q.textContent=R.amb?'Ambiance « '+AMB[R.amb.i].n+' » : objectif '+R.amb.target+' % de routes calmes, '+(R.amb.met?'atteint':'non atteint')+' ('+R.calm+' %), meilleur de '+R.amb.n+' tracé'+(R.amb.n>1?'s':'')+(R.bk&&R.bk.known?' · '+(R.bk.mode==='ville'?'zone dense':'zone peu dense')+(R.bk.strict?', boulangeries validées seulement':'')+(R.bk.cnt&&R.bk.cnt.length?' · choix par pause : '+R.bk.cnt.join(', '):''):'')+(R.bk&&R.bk.none?' · Aucune boulangerie ouverte repérée pour une pause à cette heure : essaie un autre horaire ou une zone plus large':''):''}"""
t=t[:a]+newq+t[b:]
# écran de validation
rp("if(osmOn())try{drawMap(true)}catch(e){}\n</script>",r"""/* ---------- validation des boulangeries (Profil › Compte) ---------- */
(()=>{const P=document.querySelector('.psub[data-t="Compte"]');if(!P)return;const box=document.createElement('div');
 box.innerHTML=`<h2 class="st" style="font-size:16px;margin:14px 0 0">Validation des boulangeries</h2><div class="set"><div class="row"><button type="button" id="bk_show" class="lnk">Afficher les boulangeries chargées</button></div><div id="bk_list"></div></div><p class="sub" style="font-size:12px;margin:6px 2px 0">« Validée » : proposée en priorité. « À éviter » : jamais proposée. Seule ta décision et ta note interne sont enregistrées, sur cet appareil pour l’instant.</p>`;P.appendChild(box);
 const L=box.querySelector('#bk_list');
 box.querySelector('#bk_show').onclick=()=>{const rows=(typeof ALL!=='undefined'?ALL:[]).filter(b=>b[9]&&b[9].id);if(!rows.length){L.innerHTML='<p class="sub" style="font-size:13px">Génère d’abord un tracé pour charger les boulangeries.</p>';return}
  L.innerHTML=rows.map((b,i)=>{const id=b[9].id,v=BST.get()[id]||{},s=v.s||'n';return `<div class="row" style="flex-wrap:wrap;gap:6px" data-id="${id}"><span style="flex:1 1 100%;font-weight:600;font-size:13px">${b[0].replace(/</g,'&lt;')}</span><select class="bk_s" aria-label="Statut de ${b[0].replace(/"/g,'')}"><option value="n"${s==='n'?' selected':''}>Non vérifiée</option><option value="v"${s==='v'?' selected':''}>Validée</option><option value="x"${s==='x'?' selected':''}>À éviter</option></select><input class="bk_n" placeholder="Note interne" value="${(v.n||'').replace(/"/g,'&quot;')}" style="flex:1 1 140px"></div>`}).join('')};
 L.addEventListener('change',e=>{const r=e.target.closest('[data-id]');if(!r)return;BST.set(r.dataset.id,r.querySelector('.bk_s').value,r.querySelector('.bk_n').value)});
 L.addEventListener('input',e=>{const r=e.target.closest('[data-id]');if(r&&e.target.classList.contains('bk_n')&&r.querySelector('.bk_s').value!=='n')BST.set(r.dataset.id,r.querySelector('.bk_s').value,e.target.value)})})();
if(osmOn())try{drawMap(true)}catch(e){}
</script>""")
rp("PlacesGoogle.near=async function(c,r){if(!osmOn())return _pn.call(this,c,r);const L=await osmEnsure(c,r);return L.filter(p=>hav(p,c)*1000<=r)};",
 "PlacesGoogle.near=async function(c,r){if(!osmOn())return _pn.call(this,c,r);if(typeof OSMC!=='undefined'&&OSMC.mode==='campagne'&&S.np&&RULES.budget[S.np])r=Math.max(r,Math.round(RULES.budget[S.np]*OSMR.budgetCamp/2.6*1000));const L=await osmEnsure(c,r);return L.filter(p=>hav(p,c)*1000<=r)};")
open('build_osm13.py','w').write(t)
