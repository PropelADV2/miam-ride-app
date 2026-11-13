# vers 35 : cafés cherchés par petites zones rectangulaires le long du tracé (requête légère), échec visible
s=open('/mnt/user-data/outputs/Miam ride osm - vers 34.html').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:70],s.count(a)); s=s.replace(a,b)
i=s.index("async function overpassCafe(");j=s.index("async function cafeMerge(")
NEW=r"""/* découpe un tracé en petites zones rectangulaires (~3 km) : bien plus léger pour Overpass qu'un couloir « around » */
function cafeBoxes(P,padLat,padLng){const B=[];let b=null,acc=0;
 for(let i=0;i<P.length;i++){const p=P[i];if(i)acc+=hav(P[i-1],p);
  if(!b)b={s:p.lat,n:p.lat,w:p.lng,e:p.lng};else{b.s=Math.min(b.s,p.lat);b.n=Math.max(b.n,p.lat);b.w=Math.min(b.w,p.lng);b.e=Math.max(b.e,p.lng)}
  if(acc>=3||i===P.length-1){B.push([b.s-padLat,b.w-padLng,b.n+padLat,b.e+padLng].map(x=>x.toFixed(4)).join(','));b=null;acc=0}}
 return B}
async function overpassCafe(paths,r){OSMP('Recherche des cafés…');
 const set=new Set();paths.forEach(P=>{if(P&&P.length>1)cafeBoxes(P,r/110000,r/73000).forEach(x=>set.add(x))});
 if(!set.size)return[];const q=`[out:json][timeout:20];(${[...set].map(b=>`node["amenity"="cafe"]["name"](${b});`).join('')});out tags center;`;let last='';
 for(let tour=0;tour<2;tour++){try{return await Promise.any(OVP.map(async u=>{const res=await fetchT(u,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'data='+encodeURIComponent(q)},15000);if(!res.ok)throw new Error('Overpass '+res.status);const j=await res.json();if(j.remark&&/error|timed out|memory/i.test(j.remark)&&!(j.elements||[]).length)throw new Error('Overpass surchargé');return osmClean((j.elements||[]).map(osmPlace))}))}catch(e){last=(e.errors&&e.errors[0]&&e.errors[0].message)||e.message}if(tour<1)await new Promise(r=>setTimeout(r,1000))}
 throw new Error(last)}
"""
s=s[:i]+NEW+s[j:]
# échec visible
rep("try{const C=await overpassCafe(paths,650),seen=new Set(L.map(p=>p.id));return L.concat(C.filter(p=>!seen.has(p.id)))}","try{const C=await overpassCafe(paths,650),seen=new Set(L.map(p=>p.id));S.cafeFail=false;return L.concat(C.filter(p=>!seen.has(p.id)))}")
rep("catch(e){try{osmToast('Cafés indisponibles pour l’instant : seules les boulangeries sont proposées')}catch(_){}return L}}","catch(e){S.cafeFail=true;try{osmToast('Cafés indisponibles pour l’instant')}catch(_){}return L}}")
rep(" e.textContent=tot===0?'OpenStreetMap n’a renvoyé aucune boulangerie pour cette zone.':'';e.hidden=tot!==0}"," const msg=(S.cafeFail&&kindCafe())?'Les cafés n’ont pas pu être chargés (serveur OpenStreetMap saturé). Relance le tracé dans un instant.':tot===0?'OpenStreetMap n’a renvoyé aucune boulangerie pour cette zone.':'';e.textContent=msg;e.hidden=!msg}")
open('/mnt/user-data/outputs/Miam ride osm - vers 35.html','w').write(s);print(len(s))
