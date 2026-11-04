t=open('build_osm14.py').read()
def rp(a,b):
    global t
    assert t.count(a)==1,(a[:80],t.count(a)); t=t.replace(a,b)
t=t.replace("Miam ride osm - vers 14.html","Miam ride osm - vers 15.html")
rp("path:C.map(p=>({lat:p[1],lng:p[0]}))","path:C.map(p=>({lat:p[1],lng:p[0],ele:p[2]}))")
code=r"""/* ---------- export GPX : fichier réel pour montre / GPS ---------- */
const xe=s=>String(s==null?'':s).replace(/[<>&"']/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&apos;'}[c]));
const slug=s=>String(s).normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^A-Za-z0-9 ]+/g,' ').replace(/\s+/g,' ').trim();
function gpxBuild(){const R=S.routeG||S.loopG;if(!R||!R.path||R.path.length<2)throw new Error('aucun tracé calculé');
 const c=S.cur||{},km=R.km||c.km||0,title=S.sumt||'Boucle',d=new Date(),dd=String(d.getDate()).padStart(2,'0')+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+d.getFullYear();
 const wpt=(p,n,ds,sym)=>`<wpt lat="${p.lat.toFixed(6)}" lon="${p.lng.toFixed(6)}"><name>${xe(n)}</name>${ds?`<desc>${xe(ds)}</desc>`:''}<sym>${sym}</sym></wpt>`;
 const w=[wpt(gStart(),'Départ',($('#from').value||'').trim(),'Flag, Green')];
 (c.P||[]).forEach((b,j)=>{const g=b[9];if(!g)return;let ar='';try{ar='arrivée vers '+fh(arrMin(j,b,Math.round(km)))}catch(e){}
  w.push(wpt(g,'Pause '+(j+1)+' · '+b[0],[b[1],b[6]?'Partenaire Miam Ride':'',ar].filter(Boolean).join(' · '),'Restaurant'))});
 if(S.mode==='dest'&&S.dest)w.push(wpt(S.dest,S.fast?'Arrivée':'Lieu étape',S.dest.label,'Flag, Red'));
 const nm='Miam Ride · '+title+' · '+Math.round(km)+' km',pts=R.path.map(p=>`<trkpt lat="${p.lat.toFixed(6)}" lon="${p.lng.toFixed(6)}">${p.ele!=null&&isFinite(p.ele)?`<ele>${(+p.ele).toFixed(1)}</ele>`:''}</trkpt>`).join('\n');
 const xml=`<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1" creator="Miam Ride" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n<metadata><name>${xe(nm)}</name><desc>${xe(Math.round(km)+' km'+(R.gain!=null?' · '+R.gain+' m de dénivelé':'')+' · '+((c.P||[]).length)+' pause'+(((c.P||[]).length)>1?'s':'')+' · tracé OpenStreetMap')}</desc><time>${d.toISOString()}</time></metadata>\n${w.join('\n')}\n<trk><name>${xe(nm)}</name><type>cycling</type><trkseg>\n${pts}\n</trkseg></trk>\n</gpx>\n`;
 return{xml,name:'Miam Ride - '+slug(title)+' '+Math.round(km)+' km - '+dd+'.gpx'}}
async function osmGpx(){const g=gpxBuild(),blob=new Blob([g.xml],{type:'application/gpx+xml'});window._lastGpx=g;
 try{const file=new File([blob],g.name,{type:'application/gpx+xml'});if(/Android|iPhone|iPad/i.test(navigator.userAgent)&&navigator.canShare&&navigator.canShare({files:[file]})){await navigator.share({files:[file],title:g.name});osmToast('GPX partagé : '+g.name);return}}catch(e){if(e&&e.name==='AbortError')return}
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=g.name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1500);
 osmToast('GPX enregistré : '+g.name+'. Ouvre-le avec l’appli de ta montre ou de ton GPS.')}
{const a0=addPlan;addPlan=function(k){const r=a0.apply(this,arguments);if(osmOn()&&k!=='share'){osmGpx().catch(e=>osmToast('GPX impossible : '+e.message))}return r}}
"""
rp("/* ---------- validation des boulangeries (Profil › Compte) ---------- */",code+"/* ---------- validation des boulangeries (Profil › Compte) ---------- */")
open('build_osm15.py','w').write(t)
