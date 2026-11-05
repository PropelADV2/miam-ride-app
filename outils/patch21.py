t=open('build_osm20.py').read()
def rp(a,b,n=1):
    global t
    assert t.count(a)==n,(a[:90],t.count(a)); t=t.replace(a,b)
t=t.replace("Miam ride osm - vers 20.html","Miam ride osm - vers 21.html")
# --- source : G() peut être fourni par la logique OSM
anchor="rep('const res=await this.compute(c,c,items.map(x=>x.p));res.stops=stops;return res}','const res=await this.compute(c,loop.dest||c,items.map(x=>x.p));res.stops=stops;return res}')"
rp(anchor,anchor+"""
rep("const G=()=>S.tdist?GARES.reduce(","const G=()=>(typeof trainG==='function'&&trainG())||(S.tdist?GARES.reduce(")
rep(":GARES[0];\\n",":GARES[0]);\\n")""")
# --- trajet à sens unique : « Ride and train » réutilise la logique du trajet jusqu'à un lieu
rp("if(S.mode==='dest')return osmDest(c,km,bearing);","if(S.mode==='dest'||S.mode==='train')return osmDest(c,km,bearing);")
rp("if(S.mode==='dest'&&S.dest&&R.path&&R.path.length>1)","if((S.mode==='dest'||S.mode==='train')&&S.dest&&R.path&&R.path.length>1)")
rp("(S.fast?'Arrivée : ':'Passage par : ')","(oneWay()?(S.mode==='train'?'Gare d’arrivée : ':'Arrivée : '):'Passage par : ')")
rp("(S.fast?'':' · au km '+Math.round(at))","(oneWay()?'':' · au km '+Math.round(at))")
rp("osmOn()&&S.mode==='dest'&&S.fast&&S.destKm","osmOn()&&oneWay()&&S.destKm")
rp("if(S.fast){OSMC.pre=","if(oneWay()){OSMC.pre=")
rp("async function osmDest(c,km,bearing){const D=S.dest||await destResolve();","async function osmDest(c,km,bearing){if(S.mode==='train'&&!S.dest&&S.tdist)await trainAuto();const D=S.dest||await destResolve();")
rp("if(!D)throw usrErr((","if(!D)throw usrErr(S.mode==='train'?'Tape une ville ou une gare d’arrivée dans « Où veux-tu aller ? »':(")
rp("if(S.mode==='dest'&&S.dest)w.push(wpt(S.dest,S.fast?'Arrivée':'Lieu étape',S.dest.label,'Flag, Red'));","if((S.mode==='dest'||S.mode==='train')&&S.dest)w.push(wpt(S.dest,oneWay()?(S.mode==='train'?'Gare d’arrivée':'Arrivée'):'Lieu étape',S.dest.label,'Flag, Red'));")
rp("if(S.mode==='dest'&&S.dest)add(pinEl('A','#FFD21F','#141414'),S.dest);","if((S.mode==='dest'||S.mode==='train')&&S.dest)add(pinEl(S.mode==='train'?'G':'A','#FFD21F','#141414'),S.dest);")
code=r"""/* ---------- Ride and train, temps A : gares OpenStreetMap + règles vélo (sans horaires de trains) ---------- */
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
async function trainSnap(g){osmToast('Recherche de la gare la plus proche…');let L=[];try{L=await osmStations(g,5)}catch(e){osmToast('Gares indisponibles : '+e.message);return}
 const b=L.map(s=>({s,d:hav(s,g)})).sort((x,y)=>x.d-y.d)[0];if(!b||b.d>4){S.dest=null;osmToast('Aucune gare à moins de 4 km de ce lieu : essaie une autre ville');return}setTrainDest(b.s)}
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
function trainUI(){if(S.mode==='train'&&S.dest&&!S.dest.st||S.mode==='dest'&&S.dest&&S.dest.st){S.dest=null;const t=$('#to');if(t)t.value=''}
 let old=document.getElementById('tr_sel');if(old)old.remove();if(!osmOn()||S.mode!=='train')return;const p=$('#panel');if(!p)return;const box=document.createElement('div');box.id='tr_sel';box.style.marginTop='10px';p.appendChild(box);
 if(S.tdist){const km=$('#km');if(km&&!km._tr){km._tr=1;km.addEventListener('input',()=>{S.dest=null;S.trainCands=null;trainRefreshSoon(600)})}if(S.trainCands)drawChips();trainRefreshSoon(0)}
 else box.innerHTML='<p class="sub">Tape une ville ou une gare dans « Où veux-tu aller ? » : on choisit la gare la plus proche (à moins de 4 km).</p>'+(S.dest&&S.dest.st?'<p class="sub"><b>'+xe(S.dest.label)+'</b></p>':'')}
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
"""
rp("/* ---------- validation des boulangeries (Profil › Compte) ---------- */",code+"/* ---------- validation des boulangeries (Profil › Compte) ---------- */")
open('build_osm21.py','w').write(t)
