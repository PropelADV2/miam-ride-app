# vers 32 : plus d'allers-retours dans les rues + cafés cherchés le long du tracé seulement (beaucoup plus rapide)
s=open('/mnt/user-data/outputs/Miam ride osm - vers 31.html').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:70],s.count(a)); s=s.replace(a,b)
# 1. ORS : pas de demi-tour aux points de passage
rep("preference:'recommended',options","preference:'recommended',continue_straight:true,options")
# 2. cafés : plus de requête géante autour du départ
rep("const cf=kindCafe()?`node","const cf=(kindCafe()&&pts.length>1)?`node")
rep("&&(z.k||!kindCafe()))||null}",")||null}")
L0="let L0=null;try{const pr=OSMC.pre&&OSMC.pre.p;if(pr)L0=await Promise.race([pr,new Promise(r=>setTimeout(()=>r(null),20000))])}catch(e){}"
rep(L0,L0+"if(kindCafe()&&Array.isArray(L0)){L0=await cafeMerge(L0,out.map(x=>x.path));OSMC.pre={p:Promise.resolve(L0)}}",2)
rep("r.dest=D;r.waypoints=r.mids||(r.via?[r.via]:[]);","r.dest=D;r.waypoints=r.mids||(r.via?[r.via]:[]);if(kindCafe()&&OSMC.pre){const pp=OSMC.pre.p;OSMC.pre={p:pp.then(L=>cafeMerge(L,[r.path]))}}")
# 3. allers-retours : on écarte les tracés qui repassent par la même rue en sens inverse
rep("  Object.assign(res,best,{waypoints:best.mids});","  try{const x=await despur(c,c,best);if(x!==best){bk(x);out.push(x);if(ambScore(x,km)<ambScore(best,km))best=x}}catch(e){}\n  Object.assign(res,best,{waypoints:best.mids});")
rep(" ok.sort((x,y)=>ambScore(x,ref)-ambScore(y,ref));const r=ok[0];"," ok.sort((x,y)=>ambScore(x,ref)-ambScore(y,ref));let r=ok[0];try{const x=await despur(c,D,r);if(x!==r&&ambScore(x,ref)<=ambScore(r,ref))r=x}catch(e){}")
JS=r"""<script id="v32">
/* ===== vers 32 : pas d'allers-retours + cafés le long du tracé ===== */
/* mètres parcourus deux fois, en sens inverse, sur la même rue (impasses, ronds-points ratés…) */
function backtrack(P){const out={m:0,pts:[]};if(!P||P.length<4)return out;
 const S=[];for(let i=1;i<P.length;i++){const a=P[i-1],b=P[i],d=hav(a,b)*1000,n=Math.max(1,Math.ceil(d/25));if(i===1)S.push(a);for(let k=1;k<=n;k++)S.push({lat:a.lat+(b.lat-a.lat)*k/n,lng:a.lng+(b.lng-a.lng)*k/n})}
 const kx=111320,ky=111320*Math.cos(S[0].lat*Math.PI/180),G=new Map(),key=(a,b)=>a+','+b;let n=0;
 for(let i=0;i<S.length;i++){const j3=Math.min(S.length-1,i+3),i0=Math.max(0,i-3),hx=(S[j3].lng-S[i0].lng)*ky,hy=(S[j3].lat-S[i0].lat)*kx,hl=Math.hypot(hx,hy)||1;
  const cx=Math.round(S[i].lng*ky/30),cy=Math.round(S[i].lat*kx/30);let back=false;
  for(let u=-1;u<=1&&!back;u++)for(let v=-1;v<=1&&!back;v++){const L=G.get(key(cx+u,cy+v));if(L)for(const q of L){if(i-q.i>16&&(hx*q.x+hy*q.y)/hl<-0.6){back=true;break}}}
  if(back){n++;out.pts.push(S[i])}
  const k=key(cx,cy);if(!G.has(k))G.set(k,[]);G.get(k).push({i,x:hx/hl,y:hy/hl})}
 out.m=n*25;return out}
function btv(r){if(!r||!r.path)return 0;if(r.bt==null){const b=backtrack(r.path);r.bt=b.m;r.btp=b.pts}return r.bt}
{const a0=ambScore;ambScore=function(r,k){return a0.apply(this,arguments)+btv(r)*0.08}}
/* si une impasse vient d'un point de passage, on le retire et on recalcule */
async function despur(o,d,r){if(!r||!r.mids||!r.mids.length||btv(r)<150)return r;
 const m=r.mids.filter(w=>!r.btp.some(t=>hav(w,t)<0.45));if(m.length===r.mids.length||m.length===0&&r.mids.length>2)return r;
 const x=await Promise.race([RoutingORS.compute(o,d,m,true),new Promise((_,j)=>setTimeout(()=>j(0),12000))]);
 if(x&&btv(x)<btv(r)*0.6&&Math.abs(x.km-r.km)<=Math.max(8,r.km*0.12)){x.mids=m;return x}return r}
/* cafés : seulement le long des tracés candidats (le disque autour du départ contient des milliers de cafés) */
async function overpassCafe(paths,r){OSMP('Recherche des cafés…');
 const cl=paths.filter(P=>P&&P.length>1).map(P=>{let pts=samplePath(P,1.0);if(pts.length>90){const st=Math.ceil(pts.length/90);pts=pts.filter((_,i)=>i%st===0)}const a=pts.map(p=>p.lat.toFixed(4)+','+p.lng.toFixed(4)).join(',');return `node["amenity"="cafe"]["name"](around:${r},${a});way["amenity"="cafe"]["name"](around:${r},${a});`}).join('');
 if(!cl)return[];const q=`[out:json][timeout:20];(${cl});out center tags;`;let last='';
 for(let tour=0;tour<2;tour++){try{return await Promise.any(OVP.map(async u=>{const res=await fetchT(u,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'data='+encodeURIComponent(q)},12000);if(!res.ok)throw new Error('Overpass '+res.status);const j=await res.json();return osmClean((j.elements||[]).map(osmPlace))}))}catch(e){last=(e.errors&&e.errors[0]&&e.errors[0].message)||e.message}if(tour<1)await new Promise(r=>setTimeout(r,1000))}
 throw new Error(last)}
async function cafeMerge(L,paths){if(!Array.isArray(L)||!kindCafe())return L;
 try{const C=await overpassCafe(paths,650),seen=new Set(L.map(p=>p.id));return L.concat(C.filter(p=>!seen.has(p.id)))}
 catch(e){try{osmToast('Cafés indisponibles pour l’instant : seules les boulangeries sont proposées')}catch(_){}return L}}
</script>
"""
i=s.rindex("</body>");s=s[:i]+JS+s[i:]
open('/mnt/user-data/outputs/Miam ride osm - vers 32.html','w').write(s);print(len(s))
