t=open('build_osm17.py').read()
def rp(a,b,n=1):
    global t
    assert t.count(a)==n,(a[:80],t.count(a)); t=t.replace(a,b)
t=t.replace("Miam ride osm - vers 17.html","Miam ride osm - vers 18.html")
# 1) recherche sans biais de proximité pour l'arrivée (sinon « Marseille » donne une rue proche du départ)
rp("async search(q,n){const c=gStart(),out=[]","async search(q,n,far){const c=gStart(),out=[],ll=far?'':'&lat='+c.lat+'&lon='+c.lng")
rp("+'&lang=fr&lat='+c.lat+'&lon='+c.lng+'&q='","+'&lang=fr'+ll+'&q='")
rp("+(n||1)+'&lat='+c.lat+'&lon='+c.lng+'&q='+encodeURIComponent(q),{},7000).then(async r=>{if(!r.ok)throw 0;ok++;return((await r.json()).features||[]).map(F=>({lng","+(n||1)+ll+'&q='+encodeURIComponent(q),{},7000).then(async r=>{if(!r.ok)throw 0;ok++;return((await r.json()).features||[]).map(F=>({lng")
rp("const g=(await GEO.search(v,1))[0];if(g)destSet(g)","const g=(await GEO.search(v,1,true))[0];if(g)destSet(g)")
rp("const R=await GEO.search(v,5);if(my!==seq)return;show(R,R.length?'':(GEO.fail?'Recherche indisponible (connexion). Réessaie.':'Aucun résultat : précise la ville'))},300)});\n t.addEventListener('keydown'","const R=await GEO.search(v,5,true);if(my!==seq)return;show(R,R.length?'':(GEO.fail?'Recherche indisponible (connexion). Réessaie.':'Aucun résultat : précise la ville'))},300)});\n t.addEventListener('keydown'")
# 2) boulangeries : tout le couloir autour du tracé, pas seulement 4 points
rp("const L=await osmEnsure(c,r);return L.filter(p=>hav(p,c)*1000<=r)};","const L=await osmEnsure(c,r),P=S.loopG&&S.loopG.path;if(P&&P.length>1){const sp=samplePath(P,Math.max(0.4,r/2500*0.5));return L.filter(p=>sp.some(q=>hav(p,q)*1000<=r))}return L.filter(p=>hav(p,c)*1000<=r)};")
# 3) bandeau : mode démo clairement signalé, clé saisissable sur l'accueil
code=r"""/* ---------- bandeau : tracés réels ou démo ---------- */
(()=>{const go=$('#go');if(!go)return;const bn=document.createElement('div');bn.id='osm_banner';bn.style.cssText='margin:0 0 10px;padding:10px 12px;border:2px dashed var(--ink);border-radius:16px;background:#FFF6CC;font:600 12px Poppins,sans-serif;line-height:1.4';
 bn.innerHTML='<div id="osm_bt"></div><div id="osm_bk" style="display:flex;gap:6px;margin-top:8px"><input id="osm_bkey" type="password" autocomplete="off" placeholder="Colle ta clé OpenRouteService" style="flex:1;min-width:0;border:2px solid var(--ink);border-radius:99px;padding:7px 10px;font:600 12px Poppins,sans-serif"><button type="button" id="osm_bgo" class="gps">Activer</button></div>';
 (go.closest('.ctawrap')||go.parentNode).before(bn);
 const upd=()=>{const key=!!OSMS.get('mr_orskey'),off=OSMS.get('mr_osm')==='0';bn.hidden=osmOn();$('#osm_bt').textContent=!key?'Mode démo : les tracés, les boulangeries et le lieu d’arrivée ne sont pas réels. Ajoute ta clé OpenRouteService pour utiliser les vraies données OpenStreetMap.':off?'Les tracés OpenStreetMap sont désactivés : active-les pour avoir de vraies données.':'';$('#osm_bk').style.display=key&&!off?'none':off&&key?'none':'flex';
  const b=$('#osm_bgo');b.textContent=off&&key?'Activer':'Activer'};
 const reset=()=>{OSMC.key=null;OSMC.k2=null;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;S.osmEarly=null;try{showRes();drawMap(true)}catch(e){}osmWarm()};
 $('#osm_bgo').onclick=()=>{const v=$('#osm_bkey').value.trim();if(v)OSMS.set('mr_orskey',v);if(OSMS.get('mr_orskey')){OSMS.set('mr_osm','1');const o=$('#osm_on');if(o)o.value='1';const k=$('#osm_key');if(k)k.value=OSMS.get('mr_orskey')||''}upd();reset();osmToast('Tracés OpenStreetMap activés')};
 upd();setInterval(upd,1500)})();
"""
rp("/* ---------- validation des boulangeries (Profil › Compte) ---------- */",code+"/* ---------- validation des boulangeries (Profil › Compte) ---------- */")
open('build_osm18.py','w').write(t)
