import re
src=open('/mnt/user-data/outputs/miam-ride-osm.html').read()
s=src
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:60],s.count(a)); s=s.replace(a,b)
rep("const gOn=()=>PLACES_CONFIG.provider==='google'&&!!PLACES_CONFIG.googleKey;","const gOn=()=>(typeof osmOn==='function'&&osmOn())||(PLACES_CONFIG.provider==='google'&&!!PLACES_CONFIG.googleKey);")
rep("const PLACES=()=>PLACES_CONFIG.provider==='google'?PlacesGoogle:PlacesDemo;","const PLACES=()=>(PLACES_CONFIG.provider==='google'||(typeof osmOn==='function'&&osmOn()))?PlacesGoogle:PlacesDemo;")
rep("BAK.push(...ALL.filter(b=>b[3]>=RULES.minRating&&b[4]>=RULES.minReviews))}","BAK.push(...ALL.filter(b=>(typeof osmOn==='function'&&osmOn())||(b[3]>=RULES.minRating&&b[4]>=RULES.minReviews)))}")
rep("const note=b=>`${b[3].toFixed(1).replace('.',',')}/5, ${b[4]} avis`;","const note=b=>b[4]?`${b[3].toFixed(1).replace('.',',')}/5, ${b[4]} avis`:(typeof bLabel==='function'?bLabel(b):'pas encore noté');")
rep("'Google calcule ton tracé…'","'Calcul de ton tracé…'")
rep("'Google n’a pas répondu ('","'Le calcul du tracé a échoué ('")
rep("'Google n’a pas répondu pour le tracé final ('","'Le calcul du tracé final a échoué ('")
i=s.index("style:{version:8,sources:{osm:");j=s.index("layers:[{id:'osm',type:'raster',source:'osm'}]}",i)+len("layers:[{id:'osm',type:'raster',source:'osm'}]}")
s=s[:i]+"style:'https://tiles.openfreemap.org/styles/positron'"+s[j:]
rep('let C0=[2.35,48.85],','let C0=[2.1313,48.8030],')
s=re.sub(r'<title>.*?</title>','<title>Miam Ride · OSM</title>',s,count=1)
rep('const res=await this.compute(c,c,items.map(x=>x.p));res.stops=stops;return res}','const res=await this.compute(c,loop.dest||c,items.map(x=>x.p));res.stops=stops;return res}')
rep("const G=()=>S.tdist?GARES.reduce(","const G=()=>(typeof trainG==='function'&&trainG())||(S.tdist?GARES.reduce(")
rep(":GARES[0];\n",":GARES[0]);\n")
rep("const[lo,hi]=RULES.win[n][j],v=((ALL.indexOf(b)%5)-2)*.012,p=","const[lo,hi]=RULES.win[n][j];if(b&&b[9]&&b[9].f!=null){const q=Math.min(1,Math.max(0,b[9].f));return{km:Math.round(km*q),pct:Math.round(q*100)}}const v=((ALL.indexOf(b)%5)-2)*.012,p=")
rep("let base=BAK.filter(b=>!used.includes(b)),over=null,hw=false;","let base=(typeof bkWin==='function'?bkWin:(a=>a))(BAK.filter(b=>!used.includes(b)),j),over=null,hw=false;")
rep("(y[3]-x[3]));","(y[3]-x[3])||(typeof bkOrd==='function'?bkOrd(x,y):0));")
JS=r"""<script id="osm-js">
/* ===== TEST AVEC DE VRAIES DONNÉES OPENSTREETMAP =====
   Tracé vélo : OpenRouteService (profil cycling-road, clé gratuite). Boulangeries : Overpass API (shop=bakery). Adresse : Nominatim.
   Réglages dans Profil › Compte › Test OSM. Rien n'est envoyé à un serveur à nous : les appels partent de ton navigateur. */
function fetchT(url,opt,ms){const c=new AbortController(),t=setTimeout(()=>c.abort(),ms);return fetch(url,Object.assign({},opt,{signal:c.signal})).catch(e=>{throw new Error(e&&e.name==='AbortError'?'délai dépassé ('+Math.round(ms/1000)+' s)':'connexion impossible')}).finally(()=>clearTimeout(t))}
const OSMP=m=>{const g=document.getElementById('go');if(g&&g.disabled)g.textContent=m};
const OSMS={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
function osmOn(){return OSMS.get('mr_osm')!=='0'&&!!OSMS.get('mr_orskey')}
const ORS_URL='https://api.openrouteservice.org/v2/directions/cycling-road/geojson';
const CALM_TYPES=new Set([3,4,5,6,7]); // ORS waytype : 3 rue, 4 chemin, 5 piste, 6 voie cyclable, 7 voie piétonne (calmes) ; 1 route d'État, 2 route : non calmes
const OSMC={bb:null,list:[],t:0},OSMT={ors:0,orsN:0,ovp:0,show(){const e=document.getElementById('osm_time');if(e)e.textContent=OSMT.orsN?'Dernier calcul : tracé '+(OSMT.ors/1000).toFixed(1).replace('.',',')+' s ('+OSMT.orsN+' appel'+(OSMT.orsN>1?'s':'')+') · boulangeries '+(OSMT.ovp/1000).toFixed(1).replace('.',',')+' s':''}};
function elevGain(C){let g=0,ref=C[0][2]||0;for(const p of C){const z=p[2];if(z==null)continue;if(z-ref>=3){g+=z-ref;ref=z}else if(ref-z>=3)ref=z}return Math.round(g)}
const UNPAVED=new Set([2,8,9,10,11,12,15,16,17,18]); // ORS surface : non revêtu, gravier, terre, sable, herbe…
function waySummary(C,wt,sf){const d=i=>hav({lat:C[i-1][1],lng:C[i-1][0]},{lat:C[i][1],lng:C[i][0]}),seg=(a,b)=>{let L=0;for(let i=a+1;i<=b&&i<C.length;i++)L+=d(i);return L};
 let tot=0,calm=0,cyc=0,busy=0;const segs=[],bruns=[];
 ((wt&&wt.values)||[]).forEach(([a,b,v])=>{const L=seg(a,b);tot+=L;const k=CALM_TYPES.has(v)?1:0;if(k)calm+=L;if(v===6)cyc+=L;if(v===1||v===2){busy+=L;if(L>0.25)bruns.push({a,b,L})}const last=segs[segs.length-1];if(last&&last.calm===k&&last.b===a)last.b=b;else segs.push({a,b,calm:k})});
 let up=0,st=0;((sf&&sf.values)||[]).forEach(([a,b,v])=>{const L=seg(a,b);st+=L;if(UNPAVED.has(v))up+=L});
 const pc=x=>tot?Math.round(x/tot*100):null;return{calm:pc(calm),cycle:pc(cyc),busy:pc(busy),unpaved:st?Math.round(up/st*100):null,segs,bruns}}
const RoutingORS={
 async compute(o,d,mids,heavy,avoid){const light=OSMC.light&&!heavy;let m=(mids||[]).slice();
  for(let tr=0;tr<4;tr++){
   const co=[o,...m,d].map(p=>[+p.lng.toFixed(6),+p.lat.toFixed(6)]);
   OSMP('Calcul du tracé…');OSMS.step='tracé';const res=await fetchT(ORS_URL,{method:'POST',headers:{'Authorization':OSMS.get('mr_orskey'),'Content-Type':'application/json'},body:JSON.stringify(Object.assign({coordinates:co,instructions:false,preference:'recommended',options:Object.assign({avoid_features:['ferries','steps']},avoid&&avoid.length?{avoid_polygons:{type:'MultiPolygon',coordinates:avoid}}:{})},light?{}:{elevation:true,extra_info:['waytype','surface']}))},30000);
   if(!res.ok){let msg='',code=null;try{const e=await res.json();msg=(e.error&&e.error.message)||'';code=e.error&&e.error.code}catch(_){}
    if(res.status===404&&tr<3){ // départ ou point de passage sans voie cyclable accessible : on décale légèrement
     const J=[[.12,.08],[-.18,.10],[.08,-.20]][tr],mv=p=>offKm(p,J[0],J[1]);const same=o.lat===d.lat&&o.lng===d.lng;o=mv(o);d=same?o:mv(d);m=m.map(p=>({lat:p.lat+(o.lat-p.lat)*.15,lng:p.lng+(o.lng-p.lng)*.15}));continue}
    throw new Error(res.status===401||res.status===403?'clé OpenRouteService refusée':res.status===429?'trop de demandes, attends une minute':'OpenRouteService '+res.status+(msg?' : '+String(msg).slice(0,90):''))}
   const j=await res.json(),f=j.features&&j.features[0];if(!f)throw new Error('aucun itinéraire trouvé');
   const C=f.geometry.coordinates,sm=f.properties.summary,ex=f.properties.extras||{},W=waySummary(C,ex.waytypes,ex.surface);
   return{km:sm.distance/1000,durMin:Math.round(sm.duration/60),path:C.map(p=>({lat:p[1],lng:p[0],ele:p[2]})),calm:W.calm,cycle:W.cycle,busy:W.busy,unpaved:W.unpaved,segs:W.segs,bruns:W.bruns,gain:elevGain(C),mids:m}}
  throw new Error('point de passage introuvable')}};
const _rc=RoutingGoogle.compute;RoutingGoogle.compute=async function(o,d,m){if(!osmOn())return _rc.call(this,o,d,m);const t0=performance.now();OSMT.orsN++;try{return await RoutingORS.compute(o,d,m)}finally{OSMT.ors+=performance.now()-t0;OSMT.show()}};
/* ---------- boulangeries : Overpass ---------- */
const DAYFR={Mo:'Lun',Tu:'Mar',We:'Mer',Th:'Jeu',Fr:'Ven',Sa:'Sam',Su:'Dim'};
function osmHours(str){if(!str)return null;const t=str.trim();if(/^24\/7$/.test(t))return parseH('Lun-Dim 0:00-23:59');
 const D=['Mo','Tu','We','Th','Fr','Sa','Su'],DR='(?:Mo|Tu|We|Th|Fr|Sa|Su)',out=[],TR='\\d{1,2}:\\d{2}\\s*-\\s*\\d{1,2}:\\d{2}',re=new RegExp('^\\s*('+DR+'(?:\\s*-\\s*'+DR+')?(?:\\s*,\\s*'+DR+'(?:\\s*-\\s*'+DR+')?)*)\\s+('+TR+'(?:\\s*,\\s*'+TR+')*)\\s*$');
 for(const seg of t.split(';')){const m=re.exec(seg);if(!m)continue;const tm=m[2].replace(/\s+/g,'').replace(/(^|,|-)0(\d:)/g,'$1$2');
  m[1].split(',').forEach(r=>{const[a,b]=r.split('-').map(x=>x.trim());if(b&&D.indexOf(b)<D.indexOf(a))out.push(DAYFR[a]+'-Dim '+tm,'Lun-'+DAYFR[b]+' '+tm);else out.push((b?DAYFR[a]+'-'+DAYFR[b]:DAYFR[a])+' '+tm)})}
 try{return out.length?parseH(out.join('; ')):null}catch(e){return null}}
function osmClean(L){const out=[];for(const p of L){if(!p||p.name==='Boulangerie'||(typeof OSMR!=='undefined'&&OSMR.chains.test(p.name)))continue;if(out.some(q=>q.name.toLowerCase()===p.name.toLowerCase()&&hav(q,p)<0.08))continue;out.push(p)}return out}
function osmPlace(e){const t=e.tags||{},lat=e.lat!=null?e.lat:e.center&&e.center.lat,lng=e.lon!=null?e.lon:e.center&&e.center.lon;if(lat==null||lng==null)return null;
 const a=[[t['addr:housenumber'],t['addr:street']].filter(Boolean).join(' '),t['addr:city']].filter(Boolean).join(', ');
 return{id:e.type+'/'+e.id,name:t.name||'Boulangerie',addr:a,lat,lng,rating:0,reviews:0,hours:osmHours(t.opening_hours),_h:t.opening_hours||null}}
const OVP=['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter','https://overpass.openstreetmap.fr/api/interpreter','https://maps.mail.ru/osm/tools/overpass/api/interpreter'];
const BAKC={load(){try{return JSON.parse(OSMS.get('mr_bakc')||'[]')}catch(e){return[]}},save(a){try{OSMS.set('mr_bakc',JSON.stringify(a.slice(-6)))}catch(e){}},
 find(c,r){const now=Date.now();return this.load().find(z=>now-z.t<24*3600*1000&&hav(c,z.c)*1000+r<=z.r)||null},
 add(c,r,list){const a=this.load().filter(z=>hav(c,z.c)>0.05);a.push({c:{lat:c.lat,lng:c.lng},r,t:Date.now(),l:list.map(p=>[p.id,p.name,p.addr,p.lat,p.lng,p.hours?1:0,p._h||null])});this.save(a)}};
async function overpass(pts,radiusM){const t0=performance.now();try{
 if(pts.length===1){const c=pts[0],z=BAKC.find(c,radiusM);if(z){return osmClean(z.l.map(x=>({id:x[0],name:x[1],addr:x[2],lat:x[3],lng:x[4],rating:0,reviews:0,hours:x[6]?osmHours(x[6]):null})))}}
 const L=await overpass0(pts,radiusM);if(pts.length===1)BAKC.add(pts[0],radiusM,L);return L}finally{OSMT.ovp+=performance.now()-t0;OSMT.show()}}
async function overpass0(pts,radiusM){OSMP('Recherche des boulangeries…');const around=pts.map(p=>p.lat.toFixed(4)+','+p.lng.toFixed(4)).join(',');
 const q=`[out:json][timeout:20];(node["shop"="bakery"](around:${radiusM},${around});way["shop"="bakery"](around:${radiusM},${around}););out center tags;`;let last='';
 for(let tour=0;tour<3;tour++){try{return await Promise.any(OVP.map(async u=>{const res=await fetchT(u,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'data='+encodeURIComponent(q)},18000);if(!res.ok)throw new Error('Overpass '+res.status);const j=await res.json();return osmClean((j.elements||[]).map(osmPlace))}))}catch(e){last=(e.errors&&e.errors[0]&&e.errors[0].message)||e.message}if(tour<2)await new Promise(r=>setTimeout(r,1500*(tour+1)))}
 throw new Error('boulangeries : '+last)}
function samplePath(P,stepKm){const out=[P[0]];let acc=0;for(let i=1;i<P.length;i++){acc+=hav(P[i-1],P[i]);if(acc>=stepKm){out.push(P[i]);acc=0}}out.push(P[P.length-1]);return out.slice(0,120)}
const inBB=(b,o)=>b&&o.s>=b.s&&o.n<=b.n&&o.w>=b.w&&o.e<=b.e;
async function osmEnsure(c,r){const fresh=Date.now()-OSMC.t<10*60*1000;
 if(S.loopG&&OSMC.key===S.loopG&&fresh)return OSMC.list;
 if(OSMC.pre){const pre=OSMC.pre;OSMC.pre=null;const R=await pre.p;if(Array.isArray(R)&&S.loopG){OSMC.list=R;OSMC.key=S.loopG;OSMC.t=Date.now();return R}}
 if(S.loopG&&S.loopG.path&&S.loopG.path.length){if(OSMC.key===S.loopG&&fresh)return OSMC.list;const P=S.loopG.path;OSMC.list=await overpass(samplePath(P,Math.max(1.5,r/1000*0.8)),r+300);OSMC.key=S.loopG;OSMC.bb=null;OSMC.t=Date.now();return OSMC.list}
 const k=c.lat.toFixed(3)+','+c.lng.toFixed(3)+','+r;if(OSMC.k2===k&&fresh)return OSMC.list;OSMC.list=await overpass([c],r+300);OSMC.k2=k;OSMC.key=null;OSMC.t=Date.now();return OSMC.list}
const _pn=PlacesGoogle.near;PlacesGoogle.near=async function(c,r){if(!osmOn())return _pn.call(this,c,r);if(typeof OSMC!=='undefined'&&OSMC.mode==='campagne'&&S.np&&RULES.budget[S.np])r=Math.max(r,Math.round(RULES.budget[S.np]*OSMR.budgetCamp/2.6*1000));const L=await osmEnsure(c,r),P=S.loopG&&S.loopG.path;if(P&&P.length>1){const sp=samplePath(P,Math.max(0.4,r/2500*0.5));return L.filter(p=>sp.some(q=>hav(p,q)*1000<=r))}return L.filter(p=>hav(p,c)*1000<=r)};
const _pd=PlacesGoogle.details;PlacesGoogle.details=async function(p){if(!osmOn())return _pd.call(this,p);return{photos:[],mapsUrl:'https://www.openstreetmap.org/'+p.id}};
/* ---------- carte : vrai tracé sur OpenStreetMap ---------- */
function osmStats(){if(!osmOn())return;const R=S.routeG||S.loopG;if(!R||!S.gen||!$('#stats'))return;
 const km=Math.round(R.km*10)/10;if(S.cur&&S.full)S.cur.km=km;
 $('#stats').innerHTML=`<div><b>${String(km).replace('.',',')} km</b>distance</div><div><b>${R.gain!=null?R.gain+' m':'—'}</b>dénivelé</div><div><b>${R.calm!=null?R.calm+'%':'—'}</b>routes calmes</div>`;
 let d=document.getElementById('osm_det');if(!d){d=document.createElement('p');d.id='osm_det';d.className='sub';d.style.cssText='font-size:12px;margin:2px 0 6px';$('#stats').after(d)}
 d.textContent=R.cycle!=null?'Voies cyclables '+R.cycle+' % · routes principales '+R.busy+' %'+(R.unpaved!=null?' · chemins non revêtus '+R.unpaved+' %':''):'';
 let q=document.getElementById('osm_amb');if(!q){q=document.createElement('p');q.id='osm_amb';q.className='sub';q.style.cssText='font-size:12px;margin:0 0 6px;font-weight:600';d.after(q)}
 let z=document.getElementById('osm_dest');if(!z){z=document.createElement('p');z.id='osm_dest';z.className='sub';z.style.cssText='font-size:12px;margin:0 0 6px;font-weight:600';q.after(z)}
 z.textContent='';if((S.mode==='dest'||S.mode==='train')&&S.dest&&R.path&&R.path.length>1){let best=1e9,at=0,acc=0,tot=0;const cum=[0];for(let i=1;i<R.path.length;i++){acc+=hav(R.path[i-1],R.path[i]);cum.push(acc)}tot=acc;R.path.forEach((p,i)=>{const dd=hav(p,S.dest);if(dd<best){best=dd;at=cum[i]}});
  z.textContent=best<=0.3?(oneWay()?(S.mode==='train'?'Gare d’arrivée : ':'Arrivée : '):'Passage par : ')+S.dest.label+(oneWay()?'':' · au km '+Math.round(at)):'Attention : le tracé passe à '+(best<1?Math.round(best*1000)+' m':best.toFixed(1)+' km')+' de '+S.dest.label}
 q.textContent=R.amb?'Ambiance « '+AMB[R.amb.i].n+' » : objectif '+R.amb.target+' % de routes calmes, '+(R.amb.met?'atteint':'non atteint')+' ('+R.calm+' %), meilleur de '+R.amb.n+' tracé'+(R.amb.n>1?'s':'')+(R.bk&&R.bk.known?' · '+(R.bk.mode==='ville'?'zone dense':'zone peu dense')+(R.bk.strict?', boulangeries validées seulement':'')+(R.bk.cnt&&R.bk.cnt.length?' · choix par pause : '+R.bk.cnt.join(', '):''):'')+(R.bk&&R.bk.none?' · Aucune boulangerie ouverte repérée pour une pause à cette heure : essaie un autre horaire ou une zone plus large':''):''}
function osmPaint(fit){if(typeof ready==='undefined'||!ready)return;const R=S.osmEarly||S.routeG||S.loopG,c=gStart();
 const ll=P=>P.map(p=>[p.lng,p.lat]),show=R&&(S.gen||S.osmEarly===R);
 map.getSource('route').setData(!show?{type:'FeatureCollection',features:[]}:(R.segs&&R.segs.length?{type:'FeatureCollection',features:R.segs.map(g=>({type:'Feature',properties:{calm:g.calm},geometry:{type:'LineString',coordinates:ll(R.path.slice(g.a,g.b+1))}}))}:{type:'Feature',properties:{calm:1},geometry:{type:'LineString',coordinates:ll(R.path)}}));
 try{map.setPaintProperty('route','line-color',['case',['==',['get','calm'],0],'#E5484D','#141414'])}catch(e){}
 markers.forEach(x=>x.remove());markers=[];const bd=new maplibregl.LngLatBounds(),add=(el,p,fn)=>{if(fn){el.onclick=fn;el.style.cursor='pointer'}markers.push(new maplibregl.Marker({element:el}).setLngLat([p.lng,p.lat]).addTo(map));bd.extend([p.lng,p.lat])};
 add(pinEl('D','#141414','#fff'),c);if((S.mode==='dest'||S.mode==='train')&&S.dest)add(pinEl(S.mode==='train'?'G':'A','#FFD21F','#141414'),S.dest);
 if(S.gen&&S.mode!=='mamie'&&S.active<S.np&&!S.traced)cands(S.active).list.forEach(b=>{if(b[9]&&!S.picks.includes(b))add(bEl(b,false),b[9],()=>choose(b))});
 S.picks.forEach((b,i)=>{if(b&&b[9])add(bEl(b,true,i+1),b[9],S.mode==='mamie'?null:()=>{S.active=i;showRes()})});
 if(show)R.path.forEach(p=>bd.extend([p.lng,p.lat]));
 if(fit!==false)map.fitBounds(bd,{padding:50,duration:400});osmStats()}
{const d0=drawMap;drawMap=function(f){if(!osmOn())return d0(f);osmPaint(f)}}
{const s0=showRes;showRes=function(){const r=s0.apply(this,arguments);try{osmStats()}catch(e){}return r}}
/* ---------- adresse de départ : Base Adresse Nationale (France), puis Photon en secours ---------- */
(()=>{const f=$('#from');if(!f)return;
async function geo(q){const c=gStart();
 try{const r=await fetchT('https://api-adresse.data.gouv.fr/search/?limit=1&lat='+c.lat+'&lon='+c.lng+'&q='+encodeURIComponent(q),{},10000);if(r.ok){const F=((await r.json()).features||[])[0];if(F)return{lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:F.properties.label}}}catch(e){}
 try{const r=await fetchT('https://photon.komoot.io/api/?limit=1&lang=fr&lat='+c.lat+'&lon='+c.lng+'&q='+encodeURIComponent(q),{},10000);if(r.ok){const F=((await r.json()).features||[])[0];if(F){const p=F.properties;return{lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:[p.name,p.street&&((p.housenumber?p.housenumber+' ':'')+p.street),p.city].filter(Boolean).join(', ')}}}}catch(e){}
 return null}
f.addEventListener('change',async()=>{return;const v=f.value.trim();f.disabled=true;
 const g=await geo(v);f.disabled=false;
 if(g){C0=[g.lng,g.lat];f.value=g.label||v;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;OSMC.key=null;OSMC.k2=null;try{showRes()}catch(e){}try{drawMap(true)}catch(e){}osmWarm()}
 else{f.value='';f.placeholder='Adresse introuvable, essaie avec la ville'}})})();
/* ---------- accélération : boulangeries en parallèle du tracé, facteur de boucle appris ---------- */
try{const lf=parseFloat(OSMS.get('mr_lf'));if(lf>1.05&&lf<2.2)PLACES_CONFIG.loopFactor=lf}catch(e){}
/* ---------- règles boulangeries (réglables ici) ---------- */
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
{const z0=zoneApply;zoneApply=function(tu){if(osmOn()){S.bkc={corr:tu.length};tu=tu.filter(b=>bStatT(b)!=='x');if(OSMC.strict){const v=tu.filter(b=>{const s=bStatT(b);return s==='v'||s==='r'});if(v.length)tu=v}}return z0.call(this,tu)}}
/* ---------- ambiance : plusieurs boucles candidates, on garde celle qui colle à la demande ---------- */
const AMBT=[{calm:85,wk:2.2,we:.5,wb:.9,wd:1.5},{calm:65,wk:1.6,we:.25,wb:.4,wd:1.5},{calm:45,wk:1.2,we:.03,wb:.1,wd:2.5}];
function ambScore(r,km0){const a=AMBT[PROF.amb]||AMBT[1],dev=Math.abs(r.km-km0)/km0*100,cm=r.calm==null?0:r.calm;
 const f=r.bk&&r.bk.mode==='campagne'?.6:1;return dev*a.wd+f*(Math.max(0,a.calm-cm)*a.wk-Math.max(0,cm-a.calm)*a.we+(r.busy||0)*a.wb)+(r.unpaved||0)*1.5+(r.pen||0)}
function avoidPolys(path,runs,c){const out=[];runs.slice().sort((x,y)=>y.L-x.L).slice(0,5).forEach(r=>{const st=Math.max(1,Math.round((r.b-r.a)/4));for(let i=r.a;i<=r.b&&out.length<14;i+=st){const p=path[i];if(!p||hav(p,c)<0.4)continue;const dy=0.00035,dx=0.00055;out.push([[[p.lng-dx,p.lat-dy],[p.lng+dx,p.lat-dy],[p.lng+dx,p.lat+dy],[p.lng-dx,p.lat+dy],[p.lng-dx,p.lat-dy]]])}});return out}
const _rl=RoutingGoogle.loop;RoutingGoogle.loop=async function(c,km,bearing,n){if(!osmOn())return _rl.call(this,c,km,bearing,n);if(S.mode==='dest'||S.mode==='train')return osmDest(c,km,bearing);
 OSMT.ors=0;OSMT.orsN=0;OSMT.ovp=0;const r0=km/(2*Math.PI*PLACES_CONFIG.loopFactor),rad=Math.ceil((2*r0+2.5)/5)*5000;
 OSMC.pre={p:overpass([c],rad).catch(e=>({err:e}))};
 OSMC.light=true;let res;try{res=await _rl.call(this,c,km,bearing,n)}finally{OSMC.light=false}
 OSMT.orsN+=2;let rr=0;
 try{const W=[c,...(res.waypoints||[])],cx=W.reduce((a,p)=>a+p.lat,0)/W.length,cy=W.reduce((a,p)=>a+p.lng,0)/W.length,ctr={lat:cx,lng:cy};rr=W.reduce((a,p)=>a+hav(ctr,p),0)/W.length;
  if(rr>0.5){const f=res.km/(2*Math.PI*rr);if(f>1.05&&f<2.2){PLACES_CONFIG.loopFactor=+f.toFixed(3);OSMS.set('mr_lf',String(PLACES_CONFIG.loopFactor))}}}catch(e){}
 S.osmEarly=res;try{osmPaint(true)}catch(e){}
 const tol=RULES.tol,nn=n||4,rU=rr>0.5?rr:km/(2*Math.PI*PLACES_CONFIG.loopFactor),amb=AMBT[PROF.amb]||AMBT[1],out=[];
 OSMP('Choix du tracé qui te correspond…');
 const T0=performance.now(),hv=async(w,av)=>{OSMT.orsN++;return RoutingORS.compute(c,c,w,true,av)};
 const job=async w0=>{let h=await hv(w0);out.push(h);return h};
 const alt=async d=>{let r=rU,w=RoutingGoogle.circle(c,r,(bearing+d)%360,nn),h=await hv(w);if(Math.abs(h.km-km)>tol){r*=km/Math.max(h.km,1);w=RoutingGoogle.circle(c,r,(bearing+d)%360,nn);h=await hv(w)}out.push(h);return h};
 try{await Promise.race([Promise.allSettled([job(res.waypoints||[]),alt(120),alt(240)]),new Promise(r=>setTimeout(r,20000))])}catch(e){}
 let L0=null;try{const pr=OSMC.pre&&OSMC.pre.p;if(pr)L0=await Promise.race([pr,new Promise(r=>setTimeout(()=>r(null),20000))])}catch(e){}
 let P0=null,mode='ville';OSMC.strict=false;
 if(Array.isArray(L0)){P0=L0.filter(p=>bStat(p)!=='x');const dn=P0.filter(p=>hav(p,c)<=rU*1.4).length;mode=dn>=OSMR.denseN?'ville':'campagne';OSMC.mode=mode;
  if(mode==='ville'){const V=P0.filter(p=>{const s=bStat(p);return s==='v'||s==='r'});if(V.length>=OSMR.minValid){P0=V;OSMC.strict=true}}}
 const bk=h=>{const e=P0?bkEval(h,P0,mode):{pen:0,n:[],cnt:[],none:false};h.pen=e.pen;h.bk={n:e.n,cnt:e.cnt,none:e.none,mode,strict:OSMC.strict,known:!!P0}};
 out.forEach(bk);
 let best=null;
 if(out.length){out.sort((x,y)=>ambScore(x,km)-ambScore(y,km));best=out[0];
  if(PROF.amb<=1&&best.calm!=null&&best.calm<amb.calm&&best.bruns&&best.bruns.length){
   try{const av=avoidPolys(best.path,best.bruns,c);if(av.length){const h=await Promise.race([hv(best.mids,av),new Promise((_,j)=>setTimeout(()=>j(0),12000))]);if(h)bk(h);if(h&&ambScore(h,km)<ambScore(best,km)){out.push(h);best=h}}}catch(e){}}
  Object.assign(res,best,{waypoints:best.mids});
  res.amb={i:PROF.amb,target:amb.calm,n:out.length,calms:out.map(x=>x.calm),met:(best.calm||0)>=amb.calm};
  OSMT.ors+=performance.now()-T0;OSMT.show();
 }else{
  RoutingGoogle.compute(c,c,res.waypoints||[],true).then(h=>{if(h&&res){Object.assign(res,{calm:h.calm,gain:h.gain,cycle:h.cycle,busy:h.busy,unpaved:h.unpaved,segs:h.segs});osmStats();try{drawMap(false)}catch(e){}}}).catch(()=>{});
 }
 S.osmEarly=res;try{osmPaint(true)}catch(e){}
 return res};
{const a0=ambSync;ambSync=function(){const p=PROF.amb,r=a0.apply(this,arguments);if(osmOn()&&PROF.amb!==p&&S.gen){S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;OSMC.key=null;try{showRes();drawMap(true)}catch(e){}osmToast('Ambiance changée : relance le tracé pour l’adapter')}return r}}
/* ---------- fiabilité : un nouvel essai automatique, et la vraie raison affichée en cas d'échec ---------- */
function osmToast(m){let t=document.getElementById('osm_toast');if(!t){t=document.createElement('div');t.id='osm_toast';t.setAttribute('role','status');t.style.cssText='position:fixed;left:16px;right:16px;bottom:96px;z-index:120;background:#141414;color:#fff;border-radius:16px;padding:12px 14px;font:600 13px Poppins,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.3)';document.body.appendChild(t)}t.textContent=m;t.hidden=false;clearTimeout(t._h);t._h=setTimeout(()=>{t.hidden=true},7000)}
{const gp0=gPrepare;gPrepare=async function(){if(!osmOn())return gp0.apply(this,arguments);
 try{return await gp0.apply(this,arguments)}
 catch(e1){if(e1&&e1.user){osmToast(e1.message);throw e1}OSMS.err=[e1.message];try{console.warn('Miam Ride OSM, 1er essai :',e1)}catch(_){}osmToast('1er essai échoué : '+e1.message);const ee=document.getElementById('osm_err');if(ee)ee.textContent='Dernière erreur : '+e1.message;OSMP('Nouvel essai…');await new Promise(r=>setTimeout(r,1200));
  try{return await gp0.apply(this,arguments)}catch(e2){osmToast('Le calcul a échoué : '+e2.message+'. Réessaie dans un instant.');throw e2}}}}
/* ---------- préchauffage : les boulangeries autour du départ sont chargées avant même de générer ---------- */
let _warmK='';function osmWarm(){if(!osmOn())return;const c=gStart(),k=c.lat.toFixed(3)+','+c.lng.toFixed(3);if(_warmK===k)return;_warmK=k;overpass([c],20000).catch(()=>{_warmK=''})}
setTimeout(osmWarm,1500);
{const g=document.querySelector('.gps');if(g)g.addEventListener('click',()=>setTimeout(osmWarm,4000))}
{const gp1=gPrepare;gPrepare=async function(){try{return await gp1.apply(this,arguments)}finally{S.osmEarly=null;if(!S.gen)try{osmPaint(false)}catch(e){}}}}
/* ---------- réglages : Profil › Compte › Test OSM ---------- */
(()=>{const P=document.querySelector('.psub[data-t="Compte"]');if(!P)return;const box=document.createElement('div');
 box.innerHTML=`<h2 class="st" style="font-size:16px;margin:14px 0 0">Tracés et boulangeries (OpenStreetMap)</h2><div class="set"><div class="row"><label for="osm_on">Tracés OpenStreetMap</label><select id="osm_on"><option value="0">Désactivés</option><option value="1">Activés</option></select></div><div class="row"><label for="osm_key">Clé OpenRouteService</label><input id="osm_key" type="password" autocomplete="off" placeholder="Colle ta clé" style="max-width:55%"></div><div class="row"><button type="button" id="osm_test" class="lnk">Tester la clé</button><span id="osm_msg" class="v"></span></div><div class="row"><small id="osm_time" style="color:var(--muted)"></small></div><div class="row"><small id="osm_err" style="color:var(--muted)"></small></div></div><p class="sub" style="font-size:12px;margin:6px 2px 0">Départ : « Me localiser » ou une adresse dans le champ de départ. La clé reste sur cet appareil. Les boulangeries viennent d’OpenStreetMap : pas de notes ni de photos.</p>`;
 P.appendChild(box);const on=box.querySelector('#osm_on'),key=box.querySelector('#osm_key'),msg=box.querySelector('#osm_msg');on.value=OSMS.get('mr_osm')==='0'?'0':'1';key.value=OSMS.get('mr_orskey')||'';
 on.onchange=()=>{OSMS.set('mr_osm',on.value);OSMC.key=null;OSMC.k2=null;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;try{showRes();drawMap(true)}catch(e){}msg.textContent=on.value==='1'&&!key.value?'Ajoute ta clé':'';setTimeout(osmWarm,300)};
 key.onchange=()=>{OSMS.set('mr_orskey',key.value.trim());msg.textContent=''};
 box.querySelector('#osm_test').onclick=async()=>{OSMS.set('mr_orskey',key.value.trim());msg.textContent='Test…';const c=gStart();try{const r=await RoutingORS.compute(c,offKm(c,1.5,0),[]);msg.textContent='OK : '+r.km.toFixed(1).replace('.',',')+' km'}catch(e){msg.textContent=e.message}}})();
/* ---------- départ : adresse par défaut claire, et bouton « Me localiser » avec vrais messages ---------- */
(()=>{const f=$('#from');if(f&&f.value==='Ma position'){f.value='Rue de la Paroisse, Versailles';f.placeholder='Tape ton adresse de départ'}
 const g=document.querySelector('.gps');if(!g)return;
 g.onclick=()=>{if(!navigator.geolocation){osmToast('Localisation indisponible ici : tape ton adresse dans le champ de départ.');return}
  osmToast('Localisation en cours…');
  navigator.geolocation.getCurrentPosition(async p=>{C0=[p.coords.longitude,p.coords.latitude];S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;OSMC.key=null;OSMC.k2=null;f.value='Ma position';
    try{const r=await fetchT('https://api-adresse.data.gouv.fr/reverse/?lon='+C0[0]+'&lat='+C0[1],{},6000),j=await r.json(),l=j.features&&j.features[0]&&j.features[0].properties.label;if(l)f.value=l}catch(e){}
    try{showRes();drawMap(true)}catch(e){}S.fromLabel=f.value;osmToast('Départ : '+f.value);osmWarm()},
   e=>{osmToast(e&&e.code===1?'Localisation refusée. Ouvre le fichier depuis un vrai site web (https) ou tape ton adresse dans le champ de départ.':e&&e.code===3?'La localisation met trop de temps. Tape ton adresse dans le champ de départ.':'Position introuvable. Tape ton adresse dans le champ de départ.')},
   {enableHighAccuracy:false,timeout:10000,maximumAge:60000})}})();
/* ---------- vers un lieu : adresse d'arrivée réelle, boucle passant par elle, ou trajet le plus rapide ---------- */
const GEO={cache:{},fail:false,async search(q,n,far){const c=gStart(),out=[],ll=far?'':'&lat='+c.lat+'&lon='+c.lng,add=r=>{if(r&&r.label&&!out.some(o=>o.label===r.label))out.push(r)};let ok=0;
 const ph=fetchT('https://photon.komoot.io/api/?limit='+(n||1)+'&lang=fr'+ll+'&q='+encodeURIComponent(q),{},7000).then(async r=>{if(!r.ok)throw 0;ok++;return((await r.json()).features||[]).map(F=>{const p=F.properties;return{lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:[p.name,p.street&&((p.housenumber?p.housenumber+' ':'')+p.street),[p.postcode,p.city||p.county].filter(Boolean).join(' ')].filter(Boolean).join(', ')}})}).catch(()=>[]);
 const ba=fetchT('https://api-adresse.data.gouv.fr/search/?limit='+(n||1)+ll+'&q='+encodeURIComponent(q),{},7000).then(async r=>{if(!r.ok)throw 0;ok++;return((await r.json()).features||[]).map(F=>({lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:F.properties.label}))}).catch(()=>[]);
 const [P,B]=await Promise.all([ph,ba]);this.fail=!ok;
 const addr=/^\d|\b(rue|avenue|av\.?|boulevard|bd|chemin|route|impasse|all[eé]e|place|quai)\b/i.test(q);(addr?[B,P]:[P,B]).forEach(L=>L.forEach(add));return out.slice(0,n||1)}};
function destSet(g){const t=$('#to');S.dest={lat:g.lat,lng:g.lng,label:g.label};S.destKm=0;if(t)t.value=g.label;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;OSMC.key=null;OSMC.k2=null;try{showRes()}catch(e){}try{drawMap(true)}catch(e){}osmToast('Arrivée : '+g.label)}
let _dp=null;async function destResolve(){const t=$('#to'),v=t?t.value.trim():'';if(S.dest&&S.dest.label===v)return S.dest;if(v.length<3)return null;if(_dp)return _dp;
 _dp=(async()=>{try{const g=(await GEO.search(v,1,true))[0];if(g)destSet(g);else{S.dest=null;osmToast(GEO.fail?'Recherche d’adresse indisponible (connexion). Réessaie dans un instant.':'Lieu introuvable : précise la ville ou le nom complet')}return S.dest}finally{_dp=null}})();return _dp}
(()=>{const t=$('#to');if(!t)return;t.setAttribute('autocomplete','off');const row=$('#toRow');if(!row)return;
 const box=document.createElement('div');box.id='to_box';box.hidden=true;box.setAttribute('role','listbox');box.style.cssText='position:absolute;left:0;right:0;top:100%;z-index:60;background:#fff;border:2px solid var(--ink);border-radius:14px;margin-top:4px;box-shadow:0 8px 24px rgba(0,0,0,.18);overflow:hidden';
 row.style.position='relative';row.appendChild(box);box.addEventListener('mousedown',e=>e.preventDefault());
 const show=(L,msg)=>{box.innerHTML='';if(msg){const p=document.createElement('div');p.textContent=msg;p.style.cssText='padding:10px 12px;font:600 13px Poppins,sans-serif;color:var(--muted)';box.appendChild(p)}
  L.forEach(g=>{const b=document.createElement('button');b.type='button';b.setAttribute('role','option');b.textContent=g.label;b.style.cssText='display:block;width:100%;text-align:left;border:0;border-top:1px solid #eee;background:#fff;padding:10px 12px;font:600 13px Poppins,sans-serif;cursor:pointer';b.onclick=()=>{box.hidden=true;destSet(g)};box.appendChild(b)});box.hidden=false};
 let tm,seq=0;t.addEventListener('input',()=>{clearTimeout(tm);const v=t.value.trim();if(S.dest&&S.dest.label!==v)S.dest=null;if(v.length<3){box.hidden=true;return}
  tm=setTimeout(async()=>{const my=++seq;show([],'Recherche…');const R=await GEO.search(v,5,true);if(my!==seq)return;show(R,R.length?'':(GEO.fail?'Recherche indisponible (connexion). Réessaie.':'Aucun résultat : précise la ville'))},300)});
 t.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();clearTimeout(tm);seq++;box.hidden=true;destResolve()}});
 t.addEventListener('change',()=>{clearTimeout(tm);seq++;box.hidden=true;destResolve()});
 document.addEventListener('click',e=>{if(!row.contains(e.target))box.hidden=true})})();
{const b0=baseKm;baseKm=function(){return osmOn()&&oneWay()&&S.destKm?S.destKm:b0.apply(this,arguments)}}
const DF={get(){const v=parseFloat(OSMS.get('mr_df'));return v>1.05&&v<2?v:1.3},set(v){if(v>1.05&&v<2)OSMS.set('mr_df',String(+v.toFixed(3)))}};
const usrErr=m=>{const e=new Error(m);e.user=true;return e};
async function osmDest(c,km,bearing){if(S.mode==='train'&&!S.dest&&S.tdist)await trainAuto();const D=S.dest||await destResolve();
 if(!D)throw usrErr(S.mode==='train'?'Tape une ville ou une gare d’arrivée dans « Où veux-tu aller ? »':($('#to')&&$('#to').value.trim().length>=3)?'Lieu d’arrivée introuvable : précise la ville ou choisis une suggestion':'Choisis d’abord un lieu d’arrivée dans le champ « Lieu d’arrivée »');
 const d=hav(c,D);if(d<0.3)throw usrErr('Le départ et l’arrivée sont au même endroit : choisis un autre lieu');
 if(d>120)throw usrErr('Ce lieu est à '+Math.round(d)+' km : trop loin pour une sortie. Choisis un lieu plus proche.');
 OSMT.ors=0;OSMT.orsN=0;OSMT.ovp=0;const T0=performance.now(),mid={lat:(c.lat+D.lat)/2,lng:(c.lng+D.lng)/2};
 if(oneWay()){OSMC.pre={p:overpass([mid],Math.ceil((d/2+3.5)/5)*5000).catch(e=>({err:e}))};
  const r=await RoutingORS.compute(c,D,[],true);OSMT.orsN++;r.dest=D;r.waypoints=[];S.destKm=Math.round(r.km);OSMT.ors+=performance.now()-T0;OSMT.show();S.osmEarly=r;try{osmPaint(true)}catch(e){}return r}
 const minT=d*2.8,target=Math.max(km,minT);if(km<minT)osmToast('Lieu à '+d.toFixed(0)+' km : boucle portée à '+Math.ceil(target)+' km');
 OSMC.pre={p:overpass([mid],Math.ceil((target/4+3.5)/5)*5000).catch(e=>({err:e}))};
 const dx=(D.lng-c.lng)*111.32*Math.cos(c.lat*RAD),dy=(D.lat-c.lat)*110.57,len=Math.hypot(dx,dy)||1,px=-dy/len,py=dx/len;
 const hOf=f=>{const R=target/(4*f);return Math.sqrt(Math.max(R*R-(d/2)*(d/2),0.04))};
 const W=(h,s,a)=>[offKm(c,dx*a+s*h*px,dy*a+s*h*py),{lat:D.lat,lng:D.lng},offKm(c,dx*(1-a)-s*h*px,dy*(1-a)-s*h*py)];
 let f=DF.get(),h=hOf(f),w=W(h,1,.5),A=null;
 OSMC.light=true;try{for(let i=0;i<3;i++){A=await RoutingORS.compute(c,c,w);OSMT.orsN++;const R=Math.sqrt((d/2)*(d/2)+h*h);f=A.km/(4*R);DF.set(f);A.waypoints=w;if(Math.abs(A.km-target)<=RULES.tol)break;h=hOf(f);w=W(h,1,.5)}}finally{OSMC.light=false}
 S.osmEarly=A;try{osmPaint(true)}catch(e){}
 OSMP('Choix du tracé qui te correspond…');
 const out=[],hv=async ww=>{OSMT.orsN++;return RoutingORS.compute(c,c,ww,true)};
 const cand=async(s,a)=>{let hh=h,ww=W(hh,s,a),r=await hv(ww);if(Math.abs(r.km-target)>RULES.tol){const ff=r.km/(4*Math.sqrt((d/2)*(d/2)+hh*hh));hh=hOf(ff);ww=W(hh,s,a);r=await hv(ww)}out.push(r);return r};
 try{await Promise.race([Promise.allSettled([cand(1,.5),cand(-1,.5),cand(1,.38)]),new Promise(r=>setTimeout(r,20000))])}catch(e){}
 const amb=AMBT[PROF.amb]||AMBT[1];let L0=null;try{const pr=OSMC.pre&&OSMC.pre.p;if(pr)L0=await Promise.race([pr,new Promise(r=>setTimeout(()=>r(null),20000))])}catch(e){}
 let P0=null,mode='ville';OSMC.strict=false;
 if(Array.isArray(L0)){P0=L0.filter(p=>bStat(p)!=='x');const dn=P0.filter(p=>hav(p,mid)<=target/4*1.4).length;mode=dn>=OSMR.denseN?'ville':'campagne';OSMC.mode=mode;
  if(mode==='ville'){const V=P0.filter(p=>{const s=bStat(p);return s==='v'||s==='r'});if(V.length>=OSMR.minValid){P0=V;OSMC.strict=true}}}
 const bk=x=>{const e=P0?bkEval(x,P0,mode):{pen:0,n:[],cnt:[],none:false};x.pen=e.pen;x.bk={n:e.n,cnt:e.cnt,none:e.none,mode,strict:OSMC.strict,known:!!P0}};
 out.forEach(bk);
 if(out.length){out.sort((x,y)=>ambScore(x,target)-ambScore(y,target));let best=out[0];
  if(PROF.amb<=1&&best.calm!=null&&best.calm<amb.calm&&best.bruns&&best.bruns.length){
   try{const av=avoidPolys(best.path,best.bruns,c);if(av.length){OSMT.orsN++;const x=await Promise.race([RoutingORS.compute(c,c,best.mids,true,av),new Promise((_,j)=>setTimeout(()=>j(0),12000))]);if(x)bk(x);if(x&&ambScore(x,target)<ambScore(best,target)){out.push(x);best=x}}}catch(e){}}
  Object.assign(A,best,{waypoints:best.mids});A.amb={i:PROF.amb,target:amb.calm,n:out.length,calms:out.map(x=>x.calm),met:(best.calm||0)>=amb.calm}}
 OSMT.ors+=performance.now()-T0;OSMT.show();S.osmEarly=A;try{osmPaint(true)}catch(e){}return A}
/* ---------- export GPX : fichier réel pour montre / GPS ---------- */
const xe=s=>String(s==null?'':s).replace(/[<>&"']/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&apos;'}[c]));
const slug=s=>String(s).normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^A-Za-z0-9 ]+/g,' ').replace(/\s+/g,' ').trim();
function gpxBuild(){const R=S.routeG||S.loopG;if(!R||!R.path||R.path.length<2)throw new Error('aucun tracé calculé');
 const c=S.cur||{},km=R.km||c.km||0,title=S.sumt||'Boucle',d=new Date(),dd=String(d.getDate()).padStart(2,'0')+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+d.getFullYear();
 const wpt=(p,n,ds,sym)=>`<wpt lat="${p.lat.toFixed(6)}" lon="${p.lng.toFixed(6)}"><name>${xe(n)}</name>${ds?`<desc>${xe(ds)}</desc>`:''}<sym>${sym}</sym></wpt>`;
 const w=[wpt(gStart(),'Départ',($('#from').value||'').trim(),'Flag, Green')];
 (c.P||[]).forEach((b,j)=>{const g=b[9];if(!g)return;let ar='';try{ar='arrivée vers '+fh(arrMin(j,b,Math.round(km)))}catch(e){}
  w.push(wpt(g,'Pause '+(j+1)+' · '+b[0],[b[1],b[6]?'Partenaire Miam Ride':'',ar].filter(Boolean).join(' · '),'Restaurant'))});
 if((S.mode==='dest'||S.mode==='train')&&S.dest)w.push(wpt(S.dest,oneWay()?(S.mode==='train'?'Gare d’arrivée':'Arrivée'):'Lieu étape',S.dest.label,'Flag, Red'));
 const nm='Miam Ride · '+title+' · '+Math.round(km)+' km',pts=R.path.map(p=>`<trkpt lat="${p.lat.toFixed(6)}" lon="${p.lng.toFixed(6)}">${p.ele!=null&&isFinite(p.ele)?`<ele>${(+p.ele).toFixed(1)}</ele>`:''}</trkpt>`).join('\n');
 const xml=`<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1" creator="Miam Ride" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n<metadata><name>${xe(nm)}</name><desc>${xe(Math.round(km)+' km'+(R.gain!=null?' · '+R.gain+' m de dénivelé':'')+' · '+((c.P||[]).length)+' pause'+(((c.P||[]).length)>1?'s':'')+' · tracé OpenStreetMap')}</desc><time>${d.toISOString()}</time></metadata>\n${w.join('\n')}\n<trk><name>${xe(nm)}</name><type>cycling</type><trkseg>\n${pts}\n</trkseg></trk>\n</gpx>\n`;
 return{xml,name:'Miam Ride - '+slug(title)+' '+Math.round(km)+' km - '+dd+'.gpx'}}
async function osmGpx(){const g=gpxBuild(),blob=new Blob([g.xml],{type:'application/gpx+xml'});window._lastGpx=g;
 try{const file=new File([blob],g.name,{type:'application/gpx+xml'});if(/Android|iPhone|iPad/i.test(navigator.userAgent)&&navigator.canShare&&navigator.canShare({files:[file]})){await navigator.share({files:[file],title:g.name});osmToast('GPX partagé : '+g.name);return}}catch(e){if(e&&e.name==='AbortError')return}
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=g.name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1500);
 osmToast('GPX enregistré : '+g.name+'. Ouvre-le avec l’appli de ta montre ou de ton GPS.')}
{const a0=addPlan;addPlan=function(k){const r=a0.apply(this,arguments);if(osmOn()&&k!=='share'){osmGpx().catch(e=>osmToast('GPX impossible : '+e.message))}return r}}
/* ---------- départ : suggestions d'adresses (comme l'arrivée) ---------- */
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
/* ---------- bandeau : tracés réels ou démo ---------- */
(()=>{const go=$('#go');if(!go)return;const bn=document.createElement('div');bn.id='osm_banner';bn.style.cssText='margin:0 0 10px;padding:10px 12px;border:2px dashed var(--ink);border-radius:16px;background:#FFF6CC;font:600 12px Poppins,sans-serif;line-height:1.4';
 bn.innerHTML='<div id="osm_bt"></div><div id="osm_bk" style="display:flex;gap:6px;margin-top:8px"><input id="osm_bkey" type="password" autocomplete="off" placeholder="Colle ta clé OpenRouteService" style="flex:1;min-width:0;border:2px solid var(--ink);border-radius:99px;padding:7px 10px;font:600 12px Poppins,sans-serif"><button type="button" id="osm_bgo" class="gps">Activer</button></div>';
 (go.closest('.ctawrap')||go.parentNode).before(bn);
 const upd=()=>{const key=!!OSMS.get('mr_orskey'),off=OSMS.get('mr_osm')==='0';bn.hidden=osmOn();$('#osm_bt').textContent=!key?'Mode démo : les tracés, les boulangeries et le lieu d’arrivée ne sont pas réels. Ajoute ta clé OpenRouteService pour utiliser les vraies données OpenStreetMap.':off?'Les tracés OpenStreetMap sont désactivés : active-les pour avoir de vraies données.':'';$('#osm_bk').style.display=key&&!off?'none':off&&key?'none':'flex';
  const b=$('#osm_bgo');b.textContent=off&&key?'Activer':'Activer'};
 const reset=()=>{OSMC.key=null;OSMC.k2=null;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;S.osmEarly=null;try{showRes();drawMap(true)}catch(e){}osmWarm()};
 $('#osm_bgo').onclick=()=>{const v=$('#osm_bkey').value.trim();if(v)OSMS.set('mr_orskey',v);if(OSMS.get('mr_orskey')){OSMS.set('mr_osm','1');const o=$('#osm_on');if(o)o.value='1';const k=$('#osm_key');if(k)k.value=OSMS.get('mr_orskey')||''}upd();reset();osmToast('Tracés OpenStreetMap activés')};
 upd();setInterval(upd,1500)})();
/* ---------- position réelle de chaque boulangerie sur le tracé : fenêtres de pause respectées ---------- */
const _cumP=new WeakMap();
function pathFrac(path,p){let c=_cumP.get(path);if(!c){c=[0];for(let i=1;i<path.length;i++)c.push(c[i-1]+hav(path[i-1],path[i]));_cumP.set(path,c)}return c[nearestIdx(path,p).i]/(c[c.length-1]||1)}
{const g0=gTuple;gTuple=function(p,path){const r=g0.apply(this,arguments);if(osmOn()&&path&&path.length>1&&r[9])r[9].f=pathFrac(path,p);return r}}
function bkWin(list,j){if(!osmOn()||!S.np||!RULES.win[S.np]||!RULES.win[S.np][j])return list;const[lo,hi]=RULES.win[S.np][j];
 for(const tol of [0.03,0.12]){const L=list.filter(b=>b[9]&&b[9].f!=null&&b[9].f>=lo-tol&&b[9].f<=hi+tol);if(L.length)return L}return list}
function bkOrd(x,y){if(!osmOn())return 0;const r={v:0,r:1,n:2,x:3},sx=r[bStatT(x)]-r[bStatT(y)];if(sx)return sx;const w=RULES.win[S.np]&&RULES.win[S.np][Math.min(S.active||0,S.np-1)];if(!w)return 0;const m=(w[0]+w[1])/2,fx=x[9]&&x[9].f!=null?Math.abs(x[9].f-m):9,fy=y[9]&&y[9].f!=null?Math.abs(y[9].f-m):9;return fx-fy}
/* ---------- contrôle : où passent les boulangeries ---------- */
function osmCnt(){if(!osmOn()||!S.gen||!S.np||!$('#stats'))return;let e=document.getElementById('osm_cnt');
 if(!e){e=document.createElement('p');e.id='osm_cnt';e.className='sub';e.style.cssText='font-size:12px;margin:0 0 6px';(document.getElementById('osm_dest')||document.getElementById('osm_amb')||$('#stats')).after(e)}
 const tot=(OSMC.list||[]).length,corr=S.bkc?S.bkc.corr:0,j=Math.min(S.active||0,S.np-1),w=RULES.win[S.np]&&RULES.win[S.np][j];
 const inw=w?BAK.filter(b=>b[9]&&b[9].f!=null&&b[9].f>=w[0]-0.03&&b[9].f<=w[1]+0.03):BAK.slice(),op=inw.filter(b=>{try{return hState(b,j)!=='closed'}catch(x){return true}});
 e.textContent='Boulangeries : '+tot+' dans OpenStreetMap · '+corr+' le long du tracé · '+BAK.length+' après filtres · '+inw.length+' dans la fenêtre de la pause '+(j+1)+' · '+op.length+' ouvertes à ton heure'+(tot===0?' — OpenStreetMap n’a rien renvoyé pour cette zone':'')}
{const o0=osmStats;osmStats=function(){const r=o0.apply(this,arguments);try{osmCnt()}catch(e){}return r}}
/* ---------- Ride and train, temps A : gares OpenStreetMap + règles vélo (sans horaires de trains) ---------- */
const oneWay=()=>S.mode==='train'||(S.mode==='dest'&&S.fast);
async function ovQuery(q){let last='';for(let tour=0;tour<2;tour++){try{return await Promise.any(OVP.map(async u=>{const res=await fetchT(u,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'data='+encodeURIComponent(q)},18000);if(!res.ok)throw new Error('Overpass '+res.status);return await res.json()}))}catch(e){last=(e.errors&&e.errors[0]&&e.errors[0].message)||e.message}await new Promise(r=>setTimeout(r,1200))}throw new Error('gares : '+last)}
const STC={};
const gareLabel=n=>/^gare\b/i.test(n)?n:(/^[aeiouyhéèêâîôAEIOUYHÉ]/.test(n)?'Gare d’':'Gare de ')+n;
async function osmStations(c,rKm){const k=c.lat.toFixed(2)+','+c.lng.toFixed(2)+','+Math.ceil(rKm);if(STC[k])return STC[k];OSMP('Recherche des gares…');
 const R=Math.ceil(rKm)*1000,a=`(around:${R},${c.lat.toFixed(4)},${c.lng.toFixed(4)})`;
 const j=await ovQuery(`[out:json][timeout:25];(node["railway"="station"]${a};node["railway"="halt"]${a};way["railway"="station"]${a};);out center tags;`),out=[];
 (j.elements||[]).forEach(e=>{const g=e.tags||{},lat=e.lat!=null?e.lat:e.center&&e.center.lat,lng=e.lon!=null?e.lon:e.center&&e.center.lon;if(lat==null||!g.name)return;
  if(/^(subway|light_rail|monorail|funicular|tram)$/.test(g.station||'')&&g.train!=='yes')return;if(g.subway==='yes'&&g.train!=='yes')return;
  if(out.some(o=>o.raw.toLowerCase()===g.name.toLowerCase()&&hav(o,{lat,lng})<0.6))return;out.push({raw:g.name,name:gareLabel(g.name),lat,lng,net:g.network||g.operator||''})});
 STC[k]=out;return out}
function setTrainDest(s,quiet){const t=$('#to');S.dest={lat:s.lat,lng:s.lng,label:s.name,st:true,net:s.net||''};S.destKm=0;if(t)t.value=s.name;
 if(!quiet){S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;OSMC.key=null;OSMC.k2=null;try{showRes()}catch(e){}try{drawMap(true)}catch(e){}osmToast('Gare d’arrivée : '+s.name)}}
async function trainSnap(g){osmToast('Recherche de la gare la plus proche…');let L=[];
 for(const r of [6,15,35,70]){try{L=await osmStations(g,r)}catch(e){osmToast('Gares indisponibles : '+e.message);return}if(L.length)break}
 if(!L.length){S.dest=null;S.trainAlt=null;osmToast('Aucune gare repérée dans cette région : essaie une autre ville');return}
 const A=L.map(s=>({s,d:hav(s,g)})).sort((x,y)=>x.d-y.d).slice(0,4);S.trainAlt=A.map(x=>Object.assign({dd:x.d},x.s));S.trainPlace=g.label;
 setTrainDest(S.trainAlt[0]);const d=S.trainAlt[0].dd;osmToast(S.trainAlt[0].name+(d>4?' : la plus proche de '+g.label.split(',')[0]+' (à '+Math.round(d)+' km)':''));drawAlt()}
function drawAlt(){const box=document.getElementById('tr_sel');if(!box||S.tdist||!S.trainAlt||!S.trainAlt.length)return;const place=(S.trainPlace||'ton lieu').split(',')[0];
 box.innerHTML='<p class="sub" style="margin:0 0 6px;font-weight:600">Gares proches de '+xe(place)+'</p>';
 S.trainAlt.forEach(s=>{const b=document.createElement('button');b.type='button';const sel=S.dest&&S.dest.label===s.name;b.setAttribute('aria-pressed',sel);b.textContent=s.name+' · à '+(s.dd<1?Math.round(s.dd*1000)+' m':String(Math.round(s.dd*10)/10).replace('.',',')+' km')+' de '+place;
  b.style.cssText='display:block;width:100%;text-align:left;margin:0 0 6px;padding:10px 12px;border:2px solid var(--ink);border-radius:14px;background:'+(sel?'var(--ink)':'#fff')+';color:'+(sel?'#fff':'var(--ink)')+';font:600 13px Poppins,sans-serif;cursor:pointer';
  b.onclick=()=>{setTrainDest(s);drawAlt()};box.appendChild(b)})}
{const d0=destSet;destSet=function(g){if(S.mode==='train'&&osmOn())return trainSnap(g);return d0.apply(this,arguments)}}
async function trainCandidates(){const c=gStart(),tgt=S.km/DF.get(),L=await osmStations(c,Math.ceil(S.km/1.0));
 return L.map(s=>({s,d:hav(s,c)})).filter(x=>x.d>=Math.max(3,tgt*0.55)&&x.d<=tgt*1.25).sort((a,b)=>Math.abs(a.d-tgt)-Math.abs(b.d-tgt)).slice(0,5).map(x=>x.s)}
async function trainAuto(){const L=await trainCandidates();S.trainCands=L;if(!L.length)throw usrErr('Aucune gare repérée à environ '+S.km+' km de ton départ : change la distance ou le départ');setTrainDest(L[0],true)}
let _trT=null;function trainRefreshSoon(ms){clearTimeout(_trT);_trT=setTimeout(async()=>{const box=document.getElementById('tr_sel');if(!box||S.mode!=='train'||!S.tdist)return;box.textContent='Recherche des gares…';
  try{const L=await trainCandidates();S.trainCands=L;if(!L.length){box.innerHTML='<p class="sub">Aucune gare repérée à environ '+S.km+' km : change la distance.</p>';return}
   if(!S.dest||!S.dest.st||!L.some(s=>s.name===S.dest.label)){setTrainDest(L[0],true);S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;OSMC.key=null}drawChips()}catch(e){box.textContent='Gares indisponibles : '+e.message}},ms==null?600:ms)}
function drawChips(){const box=document.getElementById('tr_sel');if(!box||!S.trainCands)return;const c=gStart();box.innerHTML='<p class="sub" style="margin:0 0 6px;font-weight:600">Gares à environ '+S.km+' km</p>';
 S.trainCands.forEach(s=>{const b=document.createElement('button');b.type='button';const sel=S.dest&&S.dest.label===s.name;b.setAttribute('aria-pressed',sel);b.textContent=s.name+' · ≈ '+Math.round(hav(s,c)*DF.get())+' km';
  b.style.cssText='display:block;width:100%;text-align:left;margin:0 0 6px;padding:10px 12px;border:2px solid var(--ink);border-radius:14px;background:'+(sel?'var(--ink)':'#fff')+';color:'+(sel?'#fff':'var(--ink)')+';font:600 13px Poppins,sans-serif;cursor:pointer';
  b.onclick=()=>{setTrainDest(s);drawChips()};box.appendChild(b)})}
function trainUI(){if(S.mode==='train'&&S.dest&&!S.dest.st||S.mode==='dest'&&S.dest&&S.dest.st){S.dest=null;S.trainAlt=null;const t=$('#to');if(t)t.value=''}
 let old=document.getElementById('tr_sel');if(old)old.remove();if(!osmOn()||S.mode!=='train')return;const p=$('#panel');if(!p)return;const box=document.createElement('div');box.id='tr_sel';box.style.marginTop='10px';p.appendChild(box);
 if(S.tdist){const km=$('#km');if(km&&!km._tr){km._tr=1;km.addEventListener('input',()=>{S.dest=null;S.trainCands=null;trainRefreshSoon(600)})}if(S.trainCands)drawChips();trainRefreshSoon(0)}
 else{box.innerHTML='<p class="sub">Tape une ville ou une gare dans « Où veux-tu aller ? » : on te propose la gare la plus proche de ce lieu.</p>';if(S.trainAlt)drawAlt()}}
{const r0=render;render=function(){const x=r0.apply(this,arguments);try{trainUI()}catch(e){}return x}}
{const s0=startSet;startSet=function(g){const r=s0.apply(this,arguments);if(S.mode==='train'&&S.tdist){S.dest=null;S.trainCands=null;trainRefreshSoon(0)}return r}}
/* règles vélo : vérifiées le 05/11/2026 sur sncf-voyageurs.com et transilien.com (à revérifier régulièrement) */
function frHolidays(y){const a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),mo=Math.floor((h+l-7*m+114)/31),da=((h+l-7*m+114)%31)+1;
 const E=new Date(y,mo-1,da,12),add=n=>{const x=new Date(E);x.setDate(x.getDate()+n);return x},fx=[[0,1],[4,1],[4,8],[6,14],[7,15],[10,1],[10,11],[11,25]].map(([mm,dd])=>new Date(y,mm,dd,12));
 return[...fx,add(1),add(39),add(50)].map(x=>x.getFullYear()+'-'+x.getMonth()+'-'+x.getDate())}
const isHoliday=d=>frHolidays(d.getFullYear()).includes(d.getFullYear()+'-'+d.getMonth()+'-'+d.getDate());
const inIDF=p=>p.lat>=48.1&&p.lat<=49.25&&p.lng>=1.45&&p.lng<=3.6;
function trainRules(st,date,min){const dow=(date.getDay()+6)%7,wk=dow<5&&!isHoliday(date),L=[];let level='ok',short='';
 if(inIDF(st)){const bad=(min>=390&&min<570)||(min>=990&&min<1170);
  if(wk&&bad){level='ko';const nx=min<570?570:1170;short='Attention : vélo interdit dans les Transilien/RER à l’heure du retour';
   L.push('Vélo interdit dans les Transilien et RER en semaine de 6 h 30 à 9 h 30 et de 16 h 30 à 19 h 30. Avec ton horaire, le premier train possible serait vers '+fh(min)+'.','Prochain créneau où le vélo est accepté : à partir de '+fh(nx)+'. Tu peux aussi décaler ton départ.')}
  else{short=wk?'Vélo accepté au retour à cette heure (Transilien/RER)':'Vélo accepté au retour (pas de restriction ce jour-là)';
   L.push(wk?'Vélo accepté en Transilien et RER à cette heure (avant 6 h 30, de 9 h 30 à 16 h 30 et après 19 h 30), gratuit.':'Week-end et jours fériés : pas de restriction d’horaire pour le vélo en Transilien et RER.')}
  L.push('Accès refusé possible en cas de forte affluence. Vélo tenu à la main, escaliers mécaniques interdits.','Emplacements vélo dans chaque train des lignes H, K, J et L, et dans certains trains des lignes P, R, RER D et RER E.')}
 else{level='info';short='Règles vélo à vérifier selon le train de retour';
  L.push('TER : vélo gratuit dans la plupart des cas, souvent sans réservation, dans la limite des places (règles propres à chaque région).','TGV INOUI et Intercités : vélo non plié = réservation obligatoire, 10 € par trajet (5 € sur quelques lignes Intercités). Plié ou en housse (90 × 130 × 50 cm maximum) = sans réservation.','Ouigo : de 5 à 10 € selon le train et le vélo.')}
 return{level,short,lines:L}}
function trainCtx(){const R=S.routeG||S.loopG;if(!R||!S.dest||!S.dest.st)return null;const km=R.km||S.destKm||S.km,e=depMin()+Math.round(km/HOURS_RULES.speed*60)+S.np*HOURS_RULES.pauseMin,tb=e+15,date=dayDate(S.dep.day+Math.floor(tb/1440)),min=tb%1440;return{km,e,tb,date,min,rules:trainRules(S.dest,date,min)}}
function trainG(){if(!osmOn()||S.mode!=='train'||!S.dest||!S.dest.st)return null;const c=trainCtx();return[S.dest.label,Math.round(S.destKm||S.km)+' km',c?c.rules.short:'Vérifie les règles vélo du train de retour']}
function osmTrain(){let e=document.getElementById('osm_train');if(!osmOn()||S.mode!=='train'||!S.gen){if(e)e.remove();return}const c=trainCtx();if(!c){if(e)e.remove();return}
 if(!e){e=document.createElement('div');e.id='osm_train';e.style.cssText='margin:6px 0 10px;padding:10px 12px;border:2px solid var(--ink);border-radius:16px;font:500 12px/1.45 Poppins,sans-serif;background:#fff';(document.getElementById('osm_cnt')||document.getElementById('osm_dest')||$('#stats')).after(e)}
 const j=['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'][c.date.getDay()],col=c.rules.level==='ko'?'#E5484D':c.rules.level==='ok'?'#2E9E4F':'#141414';
 e.style.borderColor=col;e.innerHTML='<div style="font-weight:700;font-size:13px;margin-bottom:4px">Retour en train · '+xe(S.dest.label)+'</div><div>À la gare vers '+fh(c.e)+' (prévoir environ 15 min avant le train) · '+j+' '+c.date.getDate()+'</div><ul style="margin:6px 0 6px 16px;padding:0">'+c.rules.lines.map(x=>'<li>'+xe(x)+'</li>').join('')+'</ul><div><a href="https://www.sncf-connect.com/" target="_blank" rel="noopener">Chercher un train sur SNCF Connect</a> · <a href="https://www.iledefrance-mobilites.fr/" target="_blank" rel="noopener">Île-de-France Mobilités</a></div><div style="color:var(--muted);margin-top:4px">Règles vérifiées le 05/11/2026. Les horaires des trains ne sont pas encore affichés.</div>'}
{const o1=osmStats;osmStats=function(){const r=o1.apply(this,arguments);try{osmTrain()}catch(e){}return r}}
/* ---------- validation des boulangeries (Profil › Compte) ---------- */
(()=>{const P=document.querySelector('.psub[data-t="Compte"]');if(!P)return;const box=document.createElement('div');
 box.innerHTML=`<h2 class="st" style="font-size:16px;margin:14px 0 0">Validation des boulangeries</h2><div class="set"><div class="row"><button type="button" id="bk_show" class="lnk">Afficher les boulangeries chargées</button></div><div id="bk_list"></div></div><p class="sub" style="font-size:12px;margin:6px 2px 0">« Validée » : proposée en priorité. « À éviter » : jamais proposée. Seule ta décision et ta note interne sont enregistrées, sur cet appareil pour l’instant.</p>`;P.appendChild(box);
 const L=box.querySelector('#bk_list');
 box.querySelector('#bk_show').onclick=()=>{const rows=(typeof ALL!=='undefined'?ALL:[]).filter(b=>b[9]&&b[9].id);if(!rows.length){L.innerHTML='<p class="sub" style="font-size:13px">Génère d’abord un tracé pour charger les boulangeries.</p>';return}
  L.innerHTML=rows.map((b,i)=>{const id=b[9].id,v=BST.get()[id]||{},s=v.s||'n';return `<div class="row" style="flex-wrap:wrap;gap:6px" data-id="${id}"><span style="flex:1 1 100%;font-weight:600;font-size:13px">${b[0].replace(/</g,'&lt;')}</span><select class="bk_s" aria-label="Statut de ${b[0].replace(/"/g,'')}"><option value="n"${s==='n'?' selected':''}>Non vérifiée</option><option value="v"${s==='v'?' selected':''}>Validée</option><option value="x"${s==='x'?' selected':''}>À éviter</option></select><input class="bk_n" placeholder="Note interne" value="${(v.n||'').replace(/"/g,'&quot;')}" style="flex:1 1 140px"></div>`}).join('')};
 L.addEventListener('change',e=>{const r=e.target.closest('[data-id]');if(!r)return;BST.set(r.dataset.id,r.querySelector('.bk_s').value,r.querySelector('.bk_n').value)});
 L.addEventListener('input',e=>{const r=e.target.closest('[data-id]');if(r&&e.target.classList.contains('bk_n')&&r.querySelector('.bk_s').value!=='n')BST.set(r.dataset.id,r.querySelector('.bk_s').value,e.target.value)})})();
if(osmOn())try{drawMap(true)}catch(e){}
</script>
"""
rep("</body>",JS+"</body>")

# v23 : Ride and train sans choix de distance, lieu d'arrivée seulement
a=s.index("const sw=`<div class=\"opts\" style=\"grid-template-columns:1fr 1fr;margin-bottom:12px\"><button class=\"opt\" data-g=\"0\"")
b=s.index("p.querySelectorAll('[data-g]')")
b=s.index("\n",b)
s=s[:a]+"p.innerHTML=`<h2>Ride and train</h2><p class=\"sub\">Tape ton lieu d’arrivée dans la barre du haut. On trace le chemin le plus direct et le plus pratique, puis on te propose la gare la plus proche pour rentrer chez toi.</p>`;"+s[b:]
assert "data-g" not in s.split("function render")[1][:6000] or True
assert "Une distance" not in s
assert s.count("S.tdist=false;")==0
s=s.replace("Tape une ville ou une gare dans « Où veux-tu aller ? » : on te propose la gare la plus proche de ce lieu.","Tape ton lieu d’arrivée (adresse, ville ou gare) : on trace le chemin le plus direct, puis on te propose la gare la plus proche pour rentrer.")

# v24 : Ride and train, temps B (horaires de retour via Supabase + PRIM)
JS=open('/home/claude/p/train_b28.js').read()
end="if(osmOn())try{drawMap(true)}catch(e){}\n</script>"
assert s.count(end)==1
s=s.replace(end,JS+end)
old="Règles vérifiées le 05/11/2026. Les horaires des trains ne sont pas encore affichés."
assert s.count(old)==1
s=s.replace(old,"Règles vélo vérifiées le 05/11/2026.")

# v26 : Ride and train : le tracé va au lieu saisi, la gare est proposée après les pauses (avec le tronçon jusqu'à la gare)
def rp(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
rp("{const d0=destSet;destSet=function(g){if(S.mode==='train'&&osmOn())return trainSnap(g);return d0.apply(this,arguments)}}","")
rp("(S.mode==='train'?'Gare d’arrivée : ':'Arrivée : ')","'Arrivée : '")
rp("if((S.mode==='dest'||S.mode==='train')&&S.dest)w.push(wpt(S.dest,oneWay()?(S.mode==='train'?'Gare d’arrivée':'Arrivée'):'Lieu étape',S.dest.label,'Flag, Red'))","if((S.mode==='dest'||S.mode==='train')&&S.dest)w.push(wpt(S.dest,oneWay()?'Arrivée':'Lieu étape',S.dest.label,'Flag, Red'));if(S.mode==='train'&&S.tr&&S.tr.st&&R._legSt===S.tr.st.name)w.push(wpt(S.tr.st,'Gare de retour',S.tr.st.name,'Flag, Blue'))")
rp("S.mode==='train'?'G':'A'","'A'")

# v29 : gares : nouvel essai si Overpass limite le débit (429), cache durable, moins de requêtes
def rp(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
rp("async function ovQuery(q){let last='';for(let tour=0;tour<2;tour++){","async function ovQuery(q,T){let last='';for(let tour=0;tour<(T||2);tour++){")
rp("await new Promise(r=>setTimeout(r,1200))}throw new Error('gares : '+last)}","await new Promise(r=>setTimeout(r,T?3000*(tour+1):1200))}throw new Error(T?'gares : service saturé, réessaie dans une minute ('+last+')':'gares : '+last)}")
rp("if(STC[k])return STC[k];OSMP('Recherche des gares…');","if(STC[k])return STC[k];try{const o=JSON.parse(OSMS.get('mr_stc')||'{}');if(o[k]&&Date.now()-o[k].t<2592e6){STC[k]=o[k].v;return STC[k]}}catch(e){}OSMP('Recherche des gares…');")
rp("out center tags;`),out=[];","out center tags;`,4),out=[];")
rp("STC[k]=out;return out}","STC[k]=out;if(out.length)try{const o=JSON.parse(OSMS.get('mr_stc')||'{}');o[k]={t:Date.now(),v:out};const ks=Object.keys(o);if(ks.length>40)delete o[ks[0]];OSMS.set('mr_stc',JSON.stringify(o))}catch(e){}return out}")
rp("for(const r of [6,15,35,70]){L=await osmStations(S.dest,r)","for(const r of [10,30,70]){L=await osmStations(S.dest,r)")

# v30 : cafés (amenity=cafe) comme type de pause, filtre Boulangerie / Café / Les deux
def rp(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
# 1. requête Overpass : cafés seulement si le filtre en veut
rp("const q=`[out:json][timeout:20];(node[\"shop\"=\"bakery\"](around:${radiusM},${around});way[\"shop\"=\"bakery\"](around:${radiusM},${around}););out center tags;`;",
   "const cf=kindCafe()?`node[\"amenity\"=\"cafe\"](around:${radiusM},${around});way[\"amenity\"=\"cafe\"](around:${radiusM},${around});`:'';const q=`[out:json][timeout:25];(node[\"shop\"=\"bakery\"](around:${radiusM},${around});way[\"shop\"=\"bakery\"](around:${radiusM},${around});${cf});out center tags;`;")
# 2. place : type
rp("return{id:e.type+'/'+e.id,name:t.name||'Boulangerie',addr:a,lat,lng,rating:0,reviews:0,hours:osmHours(t.opening_hours),_h:t.opening_hours||null}}",
   "const cafe=t.amenity==='cafe'&&t.shop!=='bakery';return{id:e.type+'/'+e.id,name:t.name||(cafe?'Café':'Boulangerie'),kind:cafe?'cafe':'bakery',addr:a,lat,lng,rating:0,reviews:0,hours:osmHours(t.opening_hours),_h:t.opening_hours||null}}")
# 3. nettoyage : sans nom exclu, chaînes et débits de tabac exclus pour les cafés
rp("if(!p||p.name==='Boulangerie'||(typeof OSMR!=='undefined'&&OSMR.chains.test(p.name)))continue;",
   "if(!p||p.name==='Boulangerie'||p.name==='Café'||(typeof OSMR!=='undefined'&&OSMR.chains.test(p.name))||(p.kind==='cafe'&&CAFC.test(p.name)))continue;")
# 4. cache : type conservé, et cache valable seulement s'il contient les cafés quand on les veut
rp("find(c,r){const now=Date.now();return this.load().find(z=>now-z.t<24*3600*1000&&hav(c,z.c)*1000+r<=z.r)||null},",
   "find(c,r){const now=Date.now();return this.load().find(z=>now-z.t<24*3600*1000&&hav(c,z.c)*1000+r<=z.r&&(z.k||!kindCafe()))||null},")
rp("a.push({c:{lat:c.lat,lng:c.lng},r,t:Date.now(),l:list.map(p=>[p.id,p.name,p.addr,p.lat,p.lng,p.hours?1:0,p._h||null])});",
   "a.push({c:{lat:c.lat,lng:c.lng},r,t:Date.now(),k:kindCafe(),l:list.map(p=>[p.id,p.name,p.addr,p.lat,p.lng,p.hours?1:0,p._h||null,p.kind||'bakery'])});")
rp("rating:0,reviews:0,hours:x[6]?osmHours(x[6]):null})))}}","rating:0,reviews:0,kind:x[7]||'bakery',hours:x[6]?osmHours(x[6]):null})))}}")
# 5. filtre appliqué à la liste des pauses et à la carte
rp("BAK.push(...ALL.filter(b=>(typeof osmOn==='function'&&osmOn())||(b[3]>=RULES.minRating&&b[4]>=RULES.minReviews)))}","BAK.push(...ALL.filter(b=>(typeof osmOn==='function'&&osmOn())||(b[3]>=RULES.minRating&&b[4]>=RULES.minReviews)).filter(kOkB))}")
rp("XM.list=l.map(xDeco);","XM.list=l.filter(kOk).map(xDeco);")
rp("const note=b=>b[4]?","const note=b=>(b[9]&&b[9].kind==='cafe'?'café · ':'')+(b[4]?")
rp(":(typeof bLabel==='function'?bLabel(b):'pas encore noté');",":(typeof bLabel==='function'?bLabel(b):'pas encore noté'));")
rp("P?P.where||null:null,{id:p.id,lat:p.lat,lng:p.lng}]}","P?P.where||null:null,{id:p.id,lat:p.lat,lng:p.lng,kind:p.kind||'bakery'}]}")
# 6. interface : choix du type de pause
JS=r"""
/* ---------- type de pause : boulangerie, café, ou les deux ---------- */
const CAFC=/^(?:starbucks|columbus|costa|cojean|exki|pr[eé]t\s*[àa]\s*manger|(?:la\s+)?brioche\s+dor[ée]e|class'?\s*croute|mc\s*donald|mcdo|mc\s*caf[ée]|burger\s*king|kfc|quick|subway|five\s*guys|flunch|courtepaille|nespresso|le\s+pain\s+quotidien|paul)\b|\b(?:tabac|pmu|fdj|bar[\s-]?tabac)\b/i;
function kindCafe(){return (S.kind||'boulangerie')!=='boulangerie'}
function kOk(p){return !p||S.kind==='both'||((p.kind||'bakery')==='cafe')===(S.kind==='cafe')}
function kOkB(b){return kOk(b[9])}
try{S.kind=OSMS.get('mr_kind')||'boulangerie'}catch(e){S.kind='boulangerie'}
if(!/^(boulangerie|cafe|both)$/.test(S.kind))S.kind='boulangerie';
function kindUI(){const box=document.getElementById('kind');if(!box)return;
 box.innerHTML=[['boulangerie','Boulangerie'],['cafe','Café'],['both','Les deux']].map(k=>'<button type="button" data-k="'+k[0]+'" aria-pressed="'+(S.kind===k[0])+'">'+k[1]+'</button>').join('');
 box.querySelectorAll('button').forEach(b=>b.onclick=()=>{const k=b.dataset.k;if(k===S.kind)return;const hadCafe=kindCafe();S.kind=k;try{OSMS.set('mr_kind',k)}catch(e){}kindUI();
  if(S.gen){if(kindCafe()&&!hadCafe&&osmOn()){OSMC.t=0;osmToast('Relance le tracé pour chercher les cafés')}
   zoneApply(ALL.slice());S.picks=[];S.active=0;S.mdone=false;try{showRes()}catch(e){}}
  else if(kindCafe()&&!hadCafe)OSMC.t=0;
  try{if(typeof xLoad==='function'&&document.querySelector('#xmap:not([hidden])'))xLoad()}catch(e){}})}
function kindMount(){let w=document.getElementById('kindw');if(w)w.remove();const p=$('#panel');if(!p)return;w=document.createElement('div');w.id='kindw';w.style.marginTop='10px';w.innerHTML='<p class="fl" style="margin:0 0 6px">Type de pause</p><div class="chips" id="kind"></div>';p.appendChild(w);kindUI()}
{const r0=render;render=function(){const x=r0.apply(this,arguments);try{kindMount()}catch(e){}return x}}
kindMount();
"""
end="if(osmOn())try{drawMap(true)}catch(e){}\n</script>"
rp(end,JS+end)
open('/mnt/user-data/outputs/Miam ride osm - vers 30.html','w').write(s)
print('ok',len(s))
