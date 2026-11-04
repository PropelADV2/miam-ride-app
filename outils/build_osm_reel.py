import re
src=open('/mnt/user-data/outputs/miam-ride-osm.html').read()
s=src
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:60],s.count(a)); s=s.replace(a,b)
rep("const gOn=()=>PLACES_CONFIG.provider==='google'&&!!PLACES_CONFIG.googleKey;","const gOn=()=>(typeof osmOn==='function'&&osmOn())||(PLACES_CONFIG.provider==='google'&&!!PLACES_CONFIG.googleKey);")
rep("const PLACES=()=>PLACES_CONFIG.provider==='google'?PlacesGoogle:PlacesDemo;","const PLACES=()=>(PLACES_CONFIG.provider==='google'||(typeof osmOn==='function'&&osmOn()))?PlacesGoogle:PlacesDemo;")
rep("BAK.push(...ALL.filter(b=>b[3]>=RULES.minRating&&b[4]>=RULES.minReviews))}","BAK.push(...ALL.filter(b=>(typeof osmOn==='function'&&osmOn())||(b[3]>=RULES.minRating&&b[4]>=RULES.minReviews)))}")
rep("const note=b=>`${b[3].toFixed(1).replace('.',',')}/5, ${b[4]} avis`;","const note=b=>b[4]?`${b[3].toFixed(1).replace('.',',')}/5, ${b[4]} avis`:'pas encore noté';")
rep("'Google calcule ton tracé…'","'Calcul de ton tracé…'")
rep("'Google n’a pas répondu ('","'Le calcul du tracé a échoué ('")
rep("'Google n’a pas répondu pour le tracé final ('","'Le calcul du tracé final a échoué ('")
i=s.index("style:{version:8,sources:{osm:");j=s.index("layers:[{id:'osm',type:'raster',source:'osm'}]}",i)+len("layers:[{id:'osm',type:'raster',source:'osm'}]}")
s=s[:i]+"style:'https://tiles.openfreemap.org/styles/positron'"+s[j:]
rep('let C0=[2.35,48.85],','let C0=[2.1313,48.8030],')
s=re.sub(r'<title>.*?</title>','<title>Miam Ride · test OSM</title>',s,count=1)
JS=r"""<script id="osm-js">
/* ===== TEST AVEC DE VRAIES DONNÉES OPENSTREETMAP =====
   Tracé vélo : OpenRouteService (profil cycling-road, clé gratuite). Boulangeries : Overpass API (shop=bakery). Adresse : Nominatim.
   Réglages dans Profil › Compte › Test OSM. Rien n'est envoyé à un serveur à nous : les appels partent de ton navigateur. */
function fetchT(url,opt,ms){const c=new AbortController(),t=setTimeout(()=>c.abort(),ms);return fetch(url,Object.assign({},opt,{signal:c.signal})).catch(e=>{throw new Error(e&&e.name==='AbortError'?'délai dépassé ('+Math.round(ms/1000)+' s)':'connexion impossible')}).finally(()=>clearTimeout(t))}
const OSMP=m=>{const g=document.getElementById('go');if(g&&g.disabled)g.textContent=m};
const OSMS={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
function osmOn(){return OSMS.get('mr_osm')==='1'&&!!OSMS.get('mr_orskey')}
const ORS_URL='https://api.openrouteservice.org/v2/directions/cycling-road/geojson';
const CALM_TYPES=new Set([3,4,5,6,7]); // ORS waytype : 3 rue, 4 chemin, 5 piste, 6 voie cyclable, 7 voie piétonne (calmes) ; 1 route d'État, 2 route : non calmes
const OSMC={bb:null,list:[],t:0},OSMT={ors:0,orsN:0,ovp:0,show(){const e=document.getElementById('osm_time');if(e)e.textContent=OSMT.orsN?'Dernier calcul : tracé '+(OSMT.ors/1000).toFixed(1).replace('.',',')+' s ('+OSMT.orsN+' appel'+(OSMT.orsN>1?'s':'')+') · boulangeries '+(OSMT.ovp/1000).toFixed(1).replace('.',',')+' s':''}};
function elevGain(C){let g=0,ref=C[0][2]||0;for(const p of C){const z=p[2];if(z==null)continue;if(z-ref>=3){g+=z-ref;ref=z}else if(ref-z>=3)ref=z}return Math.round(g)}
function calmShare(C,vals){const seg=(a,b)=>{let L=0;for(let i=a+1;i<=b&&i<C.length;i++)L+=hav({lat:C[i-1][1],lng:C[i-1][0]},{lat:C[i][1],lng:C[i][0]});return L};let tot=0,calm=0;(vals||[]).forEach(([a,b,v])=>{const L=seg(a,b);tot+=L;if(CALM_TYPES.has(v))calm+=L});return tot?Math.round(calm/tot*100):null}
const RoutingORS={
 async compute(o,d,mids,heavy){const light=OSMC.light&&!heavy;let m=(mids||[]).slice();
  for(let tr=0;tr<4;tr++){
   const co=[o,...m,d].map(p=>[+p.lng.toFixed(6),+p.lat.toFixed(6)]);
   OSMP('Calcul du tracé…');OSMS.step='tracé';const res=await fetchT(ORS_URL,{method:'POST',headers:{'Authorization':OSMS.get('mr_orskey'),'Content-Type':'application/json'},body:JSON.stringify(Object.assign({coordinates:co,instructions:false,preference:'recommended',options:{avoid_features:['ferries','steps']}},light?{}:{elevation:true,extra_info:['waytype']}))},30000);
   if(!res.ok){let msg='',code=null;try{const e=await res.json();msg=(e.error&&e.error.message)||'';code=e.error&&e.error.code}catch(_){}
    if(res.status===404&&tr<3){ // départ ou point de passage sans voie cyclable accessible : on décale légèrement
     const J=[[.12,.08],[-.18,.10],[.08,-.20]][tr],mv=p=>offKm(p,J[0],J[1]);const same=o.lat===d.lat&&o.lng===d.lng;o=mv(o);d=same?o:mv(d);m=m.map(p=>({lat:p.lat+(o.lat-p.lat)*.15,lng:p.lng+(o.lng-p.lng)*.15}));continue}
    throw new Error(res.status===401||res.status===403?'clé OpenRouteService refusée':res.status===429?'trop de demandes, attends une minute':'OpenRouteService '+res.status+(msg?' : '+String(msg).slice(0,90):''))}
   const j=await res.json(),f=j.features&&j.features[0];if(!f)throw new Error('aucun itinéraire trouvé');
   const C=f.geometry.coordinates,sm=f.properties.summary,wt=f.properties.extras&&f.properties.extras.waytypes;
   return{km:sm.distance/1000,durMin:Math.round(sm.duration/60),path:C.map(p=>({lat:p[1],lng:p[0]})),calm:calmShare(C,wt&&wt.values),gain:elevGain(C),mids:m}}
  throw new Error('point de passage introuvable')}};
const _rc=RoutingGoogle.compute;RoutingGoogle.compute=async function(o,d,m){if(!osmOn())return _rc.call(this,o,d,m);const t0=performance.now();OSMT.orsN++;try{return await RoutingORS.compute(o,d,m)}finally{OSMT.ors+=performance.now()-t0;OSMT.show()}};
/* ---------- boulangeries : Overpass ---------- */
const DAYFR={Mo:'Lun',Tu:'Mar',We:'Mer',Th:'Jeu',Fr:'Ven',Sa:'Sam',Su:'Dim'};
function osmHours(str){if(!str)return null;const t=str.trim();if(/^24\/7$/.test(t))return parseH('Lun-Dim 0:00-23:59');const out=[];
 for(const seg of t.split(';')){const m=/^\s*(Mo|Tu|We|Th|Fr|Sa|Su)(?:\s*-\s*(Mo|Tu|We|Th|Fr|Sa|Su))?\s+((?:\d{1,2}:\d{2}-\d{1,2}:\d{2})(?:\s*,\s*\d{1,2}:\d{2}-\d{1,2}:\d{2})*)\s*$/.exec(seg);if(!m)continue;
  out.push((m[2]?DAYFR[m[1]]+'-'+DAYFR[m[2]]:DAYFR[m[1]])+' '+m[3].replace(/\s+/g,'').replace(/\b0(\d:)/g,'$1'))}
 try{return out.length?parseH(out.join('; ')):null}catch(e){return null}}
function osmPlace(e){const t=e.tags||{},lat=e.lat!=null?e.lat:e.center&&e.center.lat,lng=e.lon!=null?e.lon:e.center&&e.center.lon;if(lat==null||lng==null)return null;
 const a=[[t['addr:housenumber'],t['addr:street']].filter(Boolean).join(' '),t['addr:city']].filter(Boolean).join(', ');
 return{id:e.type+'/'+e.id,name:t.name||'Boulangerie',addr:a,lat,lng,rating:0,reviews:0,hours:osmHours(t.opening_hours),_h:t.opening_hours||null}}
const OVP=['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter','https://overpass.openstreetmap.fr/api/interpreter','https://maps.mail.ru/osm/tools/overpass/api/interpreter'];
const BAKC={load(){try{return JSON.parse(OSMS.get('mr_bakc')||'[]')}catch(e){return[]}},save(a){try{OSMS.set('mr_bakc',JSON.stringify(a.slice(-6)))}catch(e){}},
 find(c,r){const now=Date.now();return this.load().find(z=>now-z.t<24*3600*1000&&hav(c,z.c)*1000+r<=z.r)||null},
 add(c,r,list){const a=this.load().filter(z=>hav(c,z.c)>0.05);a.push({c:{lat:c.lat,lng:c.lng},r,t:Date.now(),l:list.map(p=>[p.id,p.name,p.addr,p.lat,p.lng,p.hours?1:0,p._h||null])});this.save(a)}};
async function overpass(pts,radiusM){const t0=performance.now();try{
 if(pts.length===1){const c=pts[0],z=BAKC.find(c,radiusM);if(z){return z.l.map(x=>({id:x[0],name:x[1],addr:x[2],lat:x[3],lng:x[4],rating:0,reviews:0,hours:x[6]?osmHours(x[6]):null}))}}
 const L=await overpass0(pts,radiusM);if(pts.length===1)BAKC.add(pts[0],radiusM,L);return L}finally{OSMT.ovp+=performance.now()-t0;OSMT.show()}}
async function overpass0(pts,radiusM){OSMP('Recherche des boulangeries…');const around=pts.map(p=>p.lat.toFixed(4)+','+p.lng.toFixed(4)).join(',');
 const q=`[out:json][timeout:20];(node["shop"="bakery"](around:${radiusM},${around});way["shop"="bakery"](around:${radiusM},${around}););out center tags;`;let last='';
 for(let tour=0;tour<3;tour++){try{return await Promise.any(OVP.map(async u=>{const res=await fetchT(u,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'data='+encodeURIComponent(q)},18000);if(!res.ok)throw new Error('Overpass '+res.status);const j=await res.json();return(j.elements||[]).map(osmPlace).filter(Boolean)}))}catch(e){last=(e.errors&&e.errors[0]&&e.errors[0].message)||e.message}if(tour<2)await new Promise(r=>setTimeout(r,1500*(tour+1)))}
 throw new Error('boulangeries : '+last)}
function samplePath(P,stepKm){const out=[P[0]];let acc=0;for(let i=1;i<P.length;i++){acc+=hav(P[i-1],P[i]);if(acc>=stepKm){out.push(P[i]);acc=0}}out.push(P[P.length-1]);return out.slice(0,120)}
const inBB=(b,o)=>b&&o.s>=b.s&&o.n<=b.n&&o.w>=b.w&&o.e<=b.e;
async function osmEnsure(c,r){const fresh=Date.now()-OSMC.t<10*60*1000;
 if(S.loopG&&OSMC.key===S.loopG&&fresh)return OSMC.list;
 if(OSMC.pre){const pre=OSMC.pre;OSMC.pre=null;const R=await pre.p;if(Array.isArray(R)&&S.loopG){OSMC.list=R;OSMC.key=S.loopG;OSMC.t=Date.now();return R}}
 if(S.loopG&&S.loopG.path&&S.loopG.path.length){if(OSMC.key===S.loopG&&fresh)return OSMC.list;const P=S.loopG.path;OSMC.list=await overpass(samplePath(P,Math.max(1.5,r/1000*0.8)),r+300);OSMC.key=S.loopG;OSMC.bb=null;OSMC.t=Date.now();return OSMC.list}
 const k=c.lat.toFixed(3)+','+c.lng.toFixed(3)+','+r;if(OSMC.k2===k&&fresh)return OSMC.list;OSMC.list=await overpass([c],r+300);OSMC.k2=k;OSMC.key=null;OSMC.t=Date.now();return OSMC.list}
const _pn=PlacesGoogle.near;PlacesGoogle.near=async function(c,r){if(!osmOn())return _pn.call(this,c,r);const L=await osmEnsure(c,r);return L.filter(p=>hav(p,c)*1000<=r)};
const _pd=PlacesGoogle.details;PlacesGoogle.details=async function(p){if(!osmOn())return _pd.call(this,p);return{photos:[],mapsUrl:'https://www.openstreetmap.org/'+p.id}};
/* ---------- carte : vrai tracé sur OpenStreetMap ---------- */
function osmStats(){if(!osmOn())return;const R=S.routeG||S.loopG;if(!R||!S.gen||!$('#stats'))return;
 const km=Math.round(R.km*10)/10;if(S.cur&&S.full)S.cur.km=km;
 $('#stats').innerHTML=`<div><b>${String(km).replace('.',',')} km</b>distance</div><div><b>${R.gain!=null?R.gain+' m':'—'}</b>dénivelé</div><div><b>${R.calm!=null?R.calm+'%':'—'}</b>routes calmes</div>`}
function osmPaint(fit){if(typeof ready==='undefined'||!ready)return;const R=S.routeG||S.loopG,c=gStart();
 map.getSource('route').setData(R&&S.gen?{type:'Feature',geometry:{type:'LineString',coordinates:R.path.map(p=>[p.lng,p.lat])}}:{type:'FeatureCollection',features:[]});
 markers.forEach(x=>x.remove());markers=[];const bd=new maplibregl.LngLatBounds(),add=(el,p,fn)=>{if(fn){el.onclick=fn;el.style.cursor='pointer'}markers.push(new maplibregl.Marker({element:el}).setLngLat([p.lng,p.lat]).addTo(map));bd.extend([p.lng,p.lat])};
 add(pinEl('D','#141414','#fff'),c);
 if(S.gen&&S.mode!=='mamie'&&S.active<S.np&&!S.traced)cands(S.active).list.forEach(b=>{if(b[9]&&!S.picks.includes(b))add(bEl(b,false),b[9],()=>choose(b))});
 S.picks.forEach((b,i)=>{if(b&&b[9])add(bEl(b,true,i+1),b[9],S.mode==='mamie'?null:()=>{S.active=i;showRes()})});
 if(R&&S.gen)R.path.forEach(p=>bd.extend([p.lng,p.lat]));
 if(fit!==false)map.fitBounds(bd,{padding:50,duration:400});osmStats()}
{const d0=drawMap;drawMap=function(f){if(!osmOn())return d0(f);osmPaint(f)}}
{const s0=showRes;showRes=function(){const r=s0.apply(this,arguments);try{osmStats()}catch(e){}return r}}
/* ---------- adresse de départ : Base Adresse Nationale (France), puis Photon en secours ---------- */
(()=>{const f=$('#from');if(!f)return;
async function geo(q){const c=gStart();
 try{const r=await fetchT('https://api-adresse.data.gouv.fr/search/?limit=1&lat='+c.lat+'&lon='+c.lng+'&q='+encodeURIComponent(q),{},10000);if(r.ok){const F=((await r.json()).features||[])[0];if(F)return{lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:F.properties.label}}}catch(e){}
 try{const r=await fetchT('https://photon.komoot.io/api/?limit=1&lang=fr&lat='+c.lat+'&lon='+c.lng+'&q='+encodeURIComponent(q),{},10000);if(r.ok){const F=((await r.json()).features||[])[0];if(F){const p=F.properties;return{lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:[p.name,p.street&&((p.housenumber?p.housenumber+' ':'')+p.street),p.city].filter(Boolean).join(', ')}}}}catch(e){}
 return null}
f.addEventListener('change',async()=>{const v=f.value.trim();if(!osmOn()||v.length<3||/^ma position$/i.test(v))return;f.disabled=true;
 const g=await geo(v);f.disabled=false;
 if(g){C0=[g.lng,g.lat];f.value=g.label||v;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;OSMC.bb=null;try{showRes()}catch(e){}try{drawMap(true)}catch(e){}}
 else{f.value='';f.placeholder='Adresse introuvable, essaie avec la ville'}})})();
/* ---------- accélération : boulangeries en parallèle du tracé, facteur de boucle appris ---------- */
try{const lf=parseFloat(OSMS.get('mr_lf'));if(lf>1.05&&lf<2.2)PLACES_CONFIG.loopFactor=lf}catch(e){}
const _rl=RoutingGoogle.loop;RoutingGoogle.loop=async function(c,km,bearing,n){if(!osmOn())return _rl.call(this,c,km,bearing,n);
 OSMT.ors=0;OSMT.orsN=0;OSMT.ovp=0;const r0=km/(2*Math.PI*PLACES_CONFIG.loopFactor),rad=Math.ceil((2*r0+2.5)/5)*5000;
 OSMC.pre={p:overpass([c],rad).catch(e=>({err:e}))};
 OSMC.light=true;let res;try{res=await _rl.call(this,c,km,bearing,n)}finally{OSMC.light=false}
 RoutingGoogle.compute(c,c,res.waypoints||[],true).then(h=>{if(h&&res){res.calm=h.calm;res.gain=h.gain;osmStats()}}).catch(()=>{});
 try{const W=[c,...(res.waypoints||[])],cx=W.reduce((a,p)=>a+p.lat,0)/W.length,cy=W.reduce((a,p)=>a+p.lng,0)/W.length,ctr={lat:cx,lng:cy},rr=W.reduce((a,p)=>a+hav(ctr,p),0)/W.length;
  if(rr>0.5){const f=res.km/(2*Math.PI*rr);if(f>1.05&&f<2.2){PLACES_CONFIG.loopFactor=+f.toFixed(3);OSMS.set('mr_lf',String(PLACES_CONFIG.loopFactor))}}}catch(e){}
 return res};
/* ---------- fiabilité : un nouvel essai automatique, et la vraie raison affichée en cas d'échec ---------- */
function osmToast(m){let t=document.getElementById('osm_toast');if(!t){t=document.createElement('div');t.id='osm_toast';t.setAttribute('role','status');t.style.cssText='position:fixed;left:16px;right:16px;bottom:96px;z-index:120;background:#141414;color:#fff;border-radius:16px;padding:12px 14px;font:600 13px Poppins,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.3)';document.body.appendChild(t)}t.textContent=m;t.hidden=false;clearTimeout(t._h);t._h=setTimeout(()=>{t.hidden=true},7000)}
{const gp0=gPrepare;gPrepare=async function(){if(!osmOn())return gp0.apply(this,arguments);
 try{return await gp0.apply(this,arguments)}
 catch(e1){OSMS.err=[e1.message];try{console.warn('Miam Ride OSM, 1er essai :',e1)}catch(_){}osmToast('1er essai échoué : '+e1.message);const ee=document.getElementById('osm_err');if(ee)ee.textContent='Dernière erreur : '+e1.message;OSMP('Nouvel essai…');await new Promise(r=>setTimeout(r,1200));
  try{return await gp0.apply(this,arguments)}catch(e2){osmToast('Le calcul a échoué : '+e2.message+'. Réessaie dans un instant.');throw e2}}}}
/* ---------- réglages : Profil › Compte › Test OSM ---------- */
(()=>{const P=document.querySelector('.psub[data-t="Compte"]');if(!P)return;const box=document.createElement('div');
 box.innerHTML=`<h2 class="st" style="font-size:16px;margin:14px 0 0">Test OSM (vraies routes)</h2><div class="set"><div class="row"><label for="osm_on">Tracés OpenStreetMap</label><select id="osm_on"><option value="0">Désactivés</option><option value="1">Activés</option></select></div><div class="row"><label for="osm_key">Clé OpenRouteService</label><input id="osm_key" type="password" autocomplete="off" placeholder="Colle ta clé" style="max-width:55%"></div><div class="row"><button type="button" id="osm_test" class="lnk">Tester la clé</button><span id="osm_msg" class="v"></span></div><div class="row"><small id="osm_time" style="color:var(--muted)"></small></div><div class="row"><small id="osm_err" style="color:var(--muted)"></small></div></div><p class="sub" style="font-size:12px;margin:6px 2px 0">Départ : « Me localiser » ou une adresse dans le champ de départ. La clé reste sur cet appareil. Les boulangeries viennent d’OpenStreetMap : pas de notes ni de photos.</p>`;
 P.appendChild(box);const on=box.querySelector('#osm_on'),key=box.querySelector('#osm_key'),msg=box.querySelector('#osm_msg');on.value=OSMS.get('mr_osm')==='1'?'1':'0';key.value=OSMS.get('mr_orskey')||'';
 on.onchange=()=>{OSMS.set('mr_osm',on.value);OSMC.key=null;OSMC.k2=null;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;try{showRes();drawMap(true)}catch(e){}msg.textContent=on.value==='1'&&!key.value?'Ajoute ta clé':''};
 key.onchange=()=>{OSMS.set('mr_orskey',key.value.trim());msg.textContent=''};
 box.querySelector('#osm_test').onclick=async()=>{OSMS.set('mr_orskey',key.value.trim());msg.textContent='Test…';const c=gStart();try{const r=await RoutingORS.compute(c,offKm(c,1.5,0),[]);msg.textContent='OK : '+r.km.toFixed(1).replace('.',',')+' km'}catch(e){msg.textContent=e.message}}})();
if(osmOn())try{drawMap(true)}catch(e){}
</script>
"""
rep("</body>",JS+"</body>")
open('/mnt/user-data/outputs/miam-ride-osm-reel.html','w').write(s)
print('ok',len(s))
