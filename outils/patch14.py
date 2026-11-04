t=open('build_osm13.py').read()
def rp(a,b):
    global t
    assert t.count(a)==1,(a[:80],t.count(a)); t=t.replace(a,b)
t=t.replace("Miam ride osm - vers 13.html","Miam ride osm - vers 14.html")
rp("RoutingGoogle.loop=async function(c,km,bearing,n){if(!osmOn())return _rl.call(this,c,km,bearing,n);","RoutingGoogle.loop=async function(c,km,bearing,n){if(!osmOn())return _rl.call(this,c,km,bearing,n);if(S.mode==='dest')return osmDest(c,km,bearing);")
rp("catch(e1){OSMS.err=[e1.message];","catch(e1){if(e1&&e1.user){osmToast(e1.message);throw e1}OSMS.err=[e1.message];")
rp("add(pinEl('D','#141414','#fff'),c);","add(pinEl('D','#141414','#fff'),c);if(S.mode==='dest'&&S.dest)add(pinEl('A','#FFD21F','#141414'),S.dest);")
code=r"""/* ---------- vers un lieu : adresse d'arrivée réelle, boucle passant par elle, ou trajet le plus rapide ---------- */
const GEO={cache:{},async search(q,n){const c=gStart(),out=[],add=r=>{if(r&&!out.some(o=>o.label===r.label))out.push(r)};
 const ph=fetchT('https://photon.komoot.io/api/?limit='+(n||1)+'&lang=fr&lat='+c.lat+'&lon='+c.lng+'&q='+encodeURIComponent(q),{},10000).then(async r=>r.ok?((await r.json()).features||[]).map(F=>{const p=F.properties;return{lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:[p.name,p.street&&((p.housenumber?p.housenumber+' ':'')+p.street),p.city||p.county].filter(Boolean).join(', ')}}):[]).catch(()=>[]);
 const ba=fetchT('https://api-adresse.data.gouv.fr/search/?limit='+(n||1)+'&lat='+c.lat+'&lon='+c.lng+'&q='+encodeURIComponent(q),{},10000).then(async r=>r.ok?((await r.json()).features||[]).map(F=>({lng:F.geometry.coordinates[0],lat:F.geometry.coordinates[1],label:F.properties.label})):[]).catch(()=>[]);
 const [P,B]=await Promise.all([ph,ba]);P.forEach(add);B.forEach(add);return out.slice(0,n||1)}};
(()=>{const t=$('#to');if(!t)return;const dl=document.createElement('datalist');dl.id='to_sug';document.body.appendChild(dl);t.setAttribute('list','to_sug');t.setAttribute('autocomplete','off');
 let tm;t.addEventListener('input',()=>{clearTimeout(tm);const v=t.value.trim();if(v.length<3||!osmOn())return;tm=setTimeout(async()=>{const R=await GEO.search(v,5);GEO.cache={};dl.innerHTML='';R.forEach(r=>{GEO.cache[r.label]=r;const o=document.createElement('option');o.value=r.label;dl.appendChild(o)})},350)});
 t.addEventListener('change',async()=>{const v=t.value.trim();if(!osmOn()||v.length<3)return;let g=GEO.cache[v];if(!g){t.disabled=true;g=(await GEO.search(v,1))[0];t.disabled=false}
  if(g){S.dest={lat:g.lat,lng:g.lng,label:g.label};S.destKm=0;t.value=g.label;S.gen=false;S.picks=[];S.loopG=null;S.routeG=null;OSMC.key=null;OSMC.k2=null;try{showRes()}catch(e){}try{drawMap(true)}catch(e){}osmToast('Arrivée : '+g.label)}
  else{S.dest=null;t.value='';t.placeholder='Lieu introuvable, précise la ville'}})})();
{const b0=baseKm;baseKm=function(){return osmOn()&&S.mode==='dest'&&S.fast&&S.destKm?S.destKm:b0.apply(this,arguments)}}
const DF={get(){const v=parseFloat(OSMS.get('mr_df'));return v>1.05&&v<2?v:1.3},set(v){if(v>1.05&&v<2)OSMS.set('mr_df',String(+v.toFixed(3)))}};
const usrErr=m=>{const e=new Error(m);e.user=true;return e};
async function osmDest(c,km,bearing){const D=S.dest;
 if(!D)throw usrErr('Choisis d’abord un lieu d’arrivée dans le champ « Lieu d’arrivée »');
 const d=hav(c,D);if(d<0.3)throw usrErr('Le départ et l’arrivée sont au même endroit : choisis un autre lieu');
 if(d>120)throw usrErr('Ce lieu est à '+Math.round(d)+' km : trop loin pour une sortie. Choisis un lieu plus proche.');
 OSMT.ors=0;OSMT.orsN=0;OSMT.ovp=0;const T0=performance.now(),mid={lat:(c.lat+D.lat)/2,lng:(c.lng+D.lng)/2};
 if(S.fast){OSMC.pre={p:overpass([mid],Math.ceil((d/2+3.5)/5)*5000).catch(e=>({err:e}))};
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
"""
rp("/* ---------- validation des boulangeries (Profil › Compte) ---------- */",code+"/* ---------- validation des boulangeries (Profil › Compte) ---------- */")
rp("s=re.sub(r'<title>.*?</title>','<title>Miam Ride · OSM</title>',s,count=1)","s=re.sub(r'<title>.*?</title>','<title>Miam Ride · OSM</title>',s,count=1)\nrep('const res=await this.compute(c,c,items.map(x=>x.p));res.stops=stops;return res}','const res=await this.compute(c,loop.dest||c,items.map(x=>x.p));res.stops=stops;return res}')")
open('build_osm14.py','w').write(t)
