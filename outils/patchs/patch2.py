import re
CSS='''
.hs{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.hs div{border:2px solid var(--ink);border-radius:16px;padding:9px 10px;font-size:11.5px;font-weight:600}.hs b{display:block;font:800 18px Poppins,sans-serif}
.hm{font:800 14px Poppins,sans-serif;text-transform:uppercase;margin:18px 0 0;letter-spacing:.02em}
.hc{display:flex;width:100%;text-align:left;border:2px solid var(--ink);border-radius:18px;background:#fff;margin-top:10px;overflow:hidden;cursor:pointer;padding:0;color:var(--ink);font:inherit}
.hc .mp{flex:none;width:104px;background:var(--peach);border-right:2px solid var(--ink);display:grid;place-items:center}.hc .mp svg{width:100%;height:auto;display:block}
.hc .tx{padding:10px 12px;min-width:0;flex:1}.hc .tx small{display:block;color:var(--muted);font-size:11.5px;font-weight:600;text-transform:capitalize}.hc .tx b{display:block;font-size:15px;font-weight:800;line-height:1.2;margin:1px 0 4px}
.hc .ln{font-size:12.5px;font-weight:600}.hc .bk2{display:flex;gap:5px;align-items:flex-start;font-size:12px;margin-top:4px;line-height:1.3}.hc .bk2 svg{flex:none;margin-top:1px}
#hd{z-index:40;padding:14px 16px 28px}.rmap{border:2px solid var(--ink);border-radius:18px;background:var(--peach);overflow:hidden}.rmap svg{display:block;width:100%;height:auto}
'''
SEG='<button type="button" role="tab" data-p="j" aria-selected="false"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M12 7v5l3.5 2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>Historique</button>'
HIST_HTML='''<div class="pg pgs" id="pgHist" hidden>
    <h1>Historique</h1>
    <div class="hs" id="hsum"></div>
    <div id="hlist"></div>
    <p class="sub" style="text-align:center;font-size:11px;margin:16px 0 0">Sorties de démonstration, données fictives.</p>
  </div>
  <div class="ov" id="hd" hidden role="dialog" aria-label="Détail de la sortie"><div class="sumh"><button class="ovx" id="hdx" type="button" aria-label="Retour">←</button><h2 id="hdt">Sortie<small id="hds"></small></h2></div><div id="hdb"></div></div>
  '''
JS='''
const RIDES=[["2026-10-18","Boucle",64,2.67,520,[["Boulangerie Dupain",31]]],["2026-10-11","Boucle",82,3.33,690,[["Maison Fournil",28],["Le Pétrin du Moulin",58]]],["2026-10-04","Ride and train",71,2.92,410,[["Fournée des Prés",35]]],["2026-09-27","Vers un lieu",108,4.42,950,[["Au Fournil de Marie",38],["La Mie Dorée",74]]],["2026-09-20","Boucle",48,1.92,310,[["Boulangerie Lemaire",24]]],["2026-09-13","Laisse Mamie choisir",96,3.83,780,[["Boulangerie Dupain",40],["Pain & Co",70]]],["2026-09-06","Le plus rapide",55,2.17,360,[["Boulangerie Les Épis",27]]],["2026-08-30","Boucle",120,4.83,1100,[["Maison Gaillard",40],["Boulangerie Dupain",82]]]];
const bakOf=n=>ALL.find(b=>b[0]===n)||[n,'','',4.2,50,0,false];
const fD=d=>new Date(d+'T12:00:00').toLocaleDateString('fr-FR',{weekday:'long',day:'numeric',month:'long'});
function loopSvg(i,r,w,h,pins){const s=i*1.7+.6,N=60,pts=[];for(let k=0;k<N;k++){const t=k/N*Math.PI*2,q=1+.28*Math.sin(2*t+s)+.18*Math.sin(3*t+2*s)+.1*Math.sin(5*t+i);pts.push([Math.cos(t)*q*(1+.15*Math.sin(s)),Math.sin(t)*q*.8])}
 const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]),x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys),pad=pins?18:10,sc=Math.min((w-2*pad)/(x1-x0),(h-2*pad)/(y1-y0)),P=pts.map(p=>[(w-(x1-x0)*sc)/2+(p[0]-x0)*sc,(h-(y1-y0)*sc)/2+(p[1]-y0)*sc]);
 const d='M'+P.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L')+'Z',g=Array.from({length:5},(_,k)=>`<path d="M0 ${(k+1)*h/6} H${w}" stroke="#fff" stroke-width="${pins?4:3}"/>`).join('')+Array.from({length:5},(_,k)=>`<path d="M${(k+1)*w/6+(i%3)*4} 0 V${h}" stroke="#fff" stroke-width="${pins?4:3}"/>`).join('');
 const pn=(pins||[]).map((f,x)=>{const p=P[Math.round(f*N)%N];return `<circle cx="${p[0]}" cy="${p[1]}" r="9" fill="#FFD21F" stroke="#141414" stroke-width="2.4"/><text x="${p[0]}" y="${p[1]+3.4}" text-anchor="middle" font-size="9.5" font-weight="800">${x+1}</text>`}).join('');
 return `<svg viewBox="0 0 ${w} ${h}" aria-hidden="true">${g}<path d="${d}" fill="none" stroke="#141414" stroke-width="${pins?4.5:3.5}" stroke-linejoin="round" stroke-linecap="round"/><circle cx="${P[0][0]}" cy="${P[0][1]}" r="${pins?8:6}" fill="#141414" stroke="#fff" stroke-width="2.4"/>${pn}</svg>`}
function histRender(){const tot=RIDES.reduce((a,r)=>a+r[2],0),mo=RIDES[0][0].slice(0,7),M=RIDES.filter(r=>r[0].slice(0,7)===mo),mk=M.reduce((a,r)=>a+r[2],0),mb=new Set(M.flatMap(r=>r[5].map(x=>x[0]))).size;
 $('#hsum').innerHTML=`<div><b>${mk} km</b>ce mois-ci</div><div><b>${M.length}</b>sorties</div><div><b>${mb}</b>boulangeries</div>`;
 let h='',cur='';RIDES.forEach((r,i)=>{const m=r[0].slice(0,7);if(m!==cur){cur=m;h+=`<h2 class="hm">${new Date(m+'-15T12:00:00').toLocaleDateString('fr-FR',{month:'long',year:'numeric'})}</h2>`}
  const pins=r[5].map((p,x)=>p[1]/r[2]);
  h+=`<button type="button" class="hc" data-r="${i}" aria-label="Voir la sortie du ${fD(r[0])}"><span class="mp">${loopSvg(i,r,104,104)}</span><span class="tx"><small>${fD(r[0])}</small><b>${r[1]}</b><span class="ln">${r[2]} km · ${fmtH(r[3])} · ${r[4]} m</span>${r[5].map(p=>{const b=bakOf(p[0]);return `<span class="bk2">${GIFT}<span>${p[0]}${b[6]?' · partenaire':''}</span></span>`}).join('')}</span></button>`});
 $('#hlist').innerHTML=h+`<p class="sub" style="text-align:center;font-size:12px;margin:14px 0 0">${RIDES.length} dernières sorties sur ${ME.rides} · ${tot} km affichés</p>`;
 document.querySelectorAll('#hlist [data-r]').forEach(b=>b.onclick=()=>openRide(+b.dataset.r))}
function openRide(i){const r=RIDES[i],v=r[2]/r[3];$('#hdt').firstChild.textContent=r[1]+' ';$('#hds').textContent=fD(r[0]);
 const pins=r[5].map(p=>p[1]/r[2]);
 let st=`<li><span class="pt k">D</span><b>Départ</b><small>km 0</small></li>`;
 r[5].forEach((p,x)=>{const b=bakOf(p[0]),L=LOY[p[0]];st+=`<li><span class="pt">${x+1}</span><b>${p[0]}</b> · ${note(b)}<small>km ${p[1]} · ${Math.round(p[1]/r[2]*100)} % du parcours</small>${b[6]?`<span class="gift">${GIFT}<span>${adv(b)}</span></span><small>Passage validé · ${L?`carte de fidélité ${L.n} passages`:'compté sur ta carte'}</small>`:'<small>Pas partenaire : aucun avantage</small>'}</li>`});
 st+=`<li><span class="pt k">A</span><b>${r[1]==='Ride and train'?'Arrivée en gare':'Arrivée'}</b><small>km ${r[2]}</small></li>`;
 $('#hdb').innerHTML=`<div class="rmap">${loopSvg(i,r,320,200,pins)}</div><p class="sub" style="font-size:11px;margin:4px 2px 10px">Tracé schématique de démonstration.</p>
 <div class="sg"><div><b>${r[2]} km</b>distance</div><div><b>${fmtH(r[3])}</b>durée</div><div><b>${r[4]} m</b>dénivelé</div><div><b>${v.toFixed(1).replace('.',',')} km/h</b>vitesse moyenne</div></div>
 <h2 style="font-size:16px;margin:16px 0 0">Étapes</h2><ol class="tl">${st}</ol>
 <div class="sum2"><button class="p" type="button" data-s="again">Refaire ce tracé</button><button type="button" data-s="gpx">Télécharger le GPX</button><button type="button" data-s="share">Partager</button></div><p class="snote" id="hnote"></p>`;
 $('#hdb').querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>{$('#hnote').textContent=b.dataset.s==='again'?'Démo : le tracé serait recalculé à partir de ta position.':b.dataset.s==='gpx'?'Démo : le fichier GPX sera généré ici.':'Démo : le partage se fera ici.'});
 $('#hd').hidden=false;$('#hd').scrollTop=0;$('#hdx').focus()}
function closeRide(){$('#hd').hidden=true}
'''
for fn in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+fn;s=open(p,encoding='utf-8').read()
    def rep(a,b):
        global s
        assert a in s,(fn,a[:60]);s=s.replace(a,b,1)
    rep("</style>",CSS+"</style>")
    rep('<div class="ov" id="sum" hidden',HIST_HTML+'<div class="ov" id="sum" hidden')
    rep('<button type="button" role="tab" data-p="f"',SEG+'<button type="button" role="tab" data-p="f"')
    rep("const m={h:'pgHome',f:'pgFid',p:'pgProf'}","const m={h:'pgHome',j:'pgHist',f:'pgFid',p:'pgProf'}")
    rep("if(p==='p')profFill();","if(p==='p')profFill();if(p==='j')histRender();")
    rep("function openSum(){",JS+"function openSum(){")
    rep("$('#sumx').onclick=closeSum;","$('#sumx').onclick=closeSum;$('#hdx').onclick=closeRide;")
    rep("if(e.key==='Escape'&&!$('#sum').hidden)closeSum()","if(e.key==='Escape'){if(!$('#sum').hidden)closeSum();if(!$('#hd').hidden)closeRide()}")
    open(p,'w',encoding='utf-8').write(s)
print('ok')
