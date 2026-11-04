import re
CSS='''
.tabbar button{position:relative}.tabbar .rdot{display:none;position:absolute;top:4px;right:calc(50% - 20px);width:10px;height:10px;border-radius:50%;background:#E5432D;border:2px solid #fff}.tabbar.rec .rdot{display:block;animation:bl 1.2s infinite}@keyframes bl{50%{opacity:.25}}
.rb{display:block;margin:18px auto 8px;width:168px;height:168px;border-radius:50%;border:3px solid var(--ink);background:var(--yellow);box-shadow:0 6px 0 var(--ink);font:800 22px Poppins,sans-serif;text-transform:uppercase;cursor:pointer;color:var(--ink)}.rb:active{transform:translateY(4px);box-shadow:0 2px 0 var(--ink)}
.rt{text-align:center;font:800 56px Poppins,sans-serif;letter-spacing:-.02em;line-height:1;margin:6px 0 2px;font-variant-numeric:tabular-nums}.rs{text-align:center;font-weight:600;font-size:12.5px;color:var(--muted)}
.rg{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}.rg div{border:2px solid var(--ink);border-radius:16px;padding:10px 12px;font-size:12px;font-weight:600}.rg b{display:block;font:800 22px Poppins,sans-serif;font-variant-numeric:tabular-nums}
.rbtn{display:flex;gap:8px;margin-top:12px}.rbtn button{flex:1;border:2px solid var(--ink);background:#fff;border-radius:99px;padding:12px;font:800 14px Poppins,sans-serif;cursor:pointer;color:var(--ink)}.rbtn button.k{background:var(--ink);color:#fff}.rbtn button.y{background:var(--yellow)}
.rlive{border:2px solid var(--ink);border-radius:18px;background:var(--peach);margin-top:12px;overflow:hidden}.rlive svg{display:block;width:100%;height:auto}
.rst{border:2px solid var(--ink);border-radius:16px;padding:10px 12px;margin-top:10px;font-size:13px}.rst select{width:100%;border:2px solid var(--ink);border-radius:12px;padding:8px;font:600 13px Poppins,sans-serif;background:#fff;margin-top:8px}
.rtip{font-size:12px;color:var(--muted);margin:10px 2px 0;line-height:1.4}.rname{width:100%;border:2px solid var(--ink);border-radius:12px;padding:10px 12px;font:700 15px Poppins,sans-serif;margin:8px 0 0}
'''
ICON='<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="12" cy="12" r="4.2" fill="currentColor"/></svg>'
BTN=f'<button type="button" role="tab" data-p="r" aria-selected="false">{ICON}<i class="rdot"></i>Enregistrer</button>'
REC_HTML='''<div class="pg pgs" id="pgRec" hidden>
    <h1>Enregistrer</h1>
    <div id="recb"></div>
  </div>
  '''
JS='''
const REC={st:'idle',t:0,d:0,up:0,pts:[[0,0]],hd:.6,stops:[],acc:1,iv:null,v:0,name:'Sortie libre'};
const pad2=n=>String(n).padStart(2,'0'),clk=s=>`${pad2(Math.floor(s/3600))}:${pad2(Math.floor(s/60)%60)}:${pad2(Math.floor(s)%60)}`;
function recSvg(pts,w,h){if(pts.length<2)return `<svg viewBox="0 0 ${w} ${h}" aria-hidden="true"><rect width="${w}" height="${h}" fill="none"/></svg>`;const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]),x0=Math.min(...xs),x1=Math.max(...xs),y0=Math.min(...ys),y1=Math.max(...ys),sc=Math.min((w-40)/Math.max(x1-x0,.05),(h-40)/Math.max(y1-y0,.05)),X=p=>(w-(x1-x0)*sc)/2+(p[0]-x0)*sc,Y=p=>(h-(y1-y0)*sc)/2+(p[1]-y0)*sc;
 const d='M'+pts.map(p=>X(p).toFixed(1)+' '+Y(p).toFixed(1)).join(' L'),a=pts[0],b=pts[pts.length-1];
 const g=Array.from({length:4},(_,k)=>`<path d="M0 ${(k+1)*h/5} H${w}" stroke="#fff" stroke-width="3"/><path d="M${(k+1)*w/5} 0 V${h}" stroke="#fff" stroke-width="3"/>`).join('');
 const st=REC.stops.map((s,i)=>`<circle cx="${X(s.p)}" cy="${Y(s.p)}" r="9" fill="#FFD21F" stroke="#141414" stroke-width="2.4"/><text x="${X(s.p)}" y="${Y(s.p)+3.4}" text-anchor="middle" font-size="9.5" font-weight="800">${i+1}</text>`).join('');
 return `<svg viewBox="0 0 ${w} ${h}" aria-hidden="true">${g}<path d="${d}" fill="none" stroke="#141414" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/><circle cx="${X(a)}" cy="${Y(a)}" r="6" fill="#141414" stroke="#fff" stroke-width="2"/>${st}<circle cx="${X(b)}" cy="${Y(b)}" r="7" fill="#E5432D" stroke="#fff" stroke-width="2.5"/></svg>`}
function recTick(){if(REC.st!=='run')return;const dt=REC.acc;REC.t+=dt;REC.v=24+3*Math.sin(REC.t/40)+Math.sin(REC.t/7);const dd=REC.v*dt/3600;REC.d+=dd;REC.up+=dd*8*(.6+.4*Math.sin(REC.t/60))*1;
 for(let k=0;k<Math.max(1,Math.round(dt/10));k++){REC.hd+=(Math.sin(REC.t/90+k)*.05)+.012;const stp=dd/Math.max(1,Math.round(dt/10));const l=REC.pts[REC.pts.length-1];REC.pts.push([l[0]+Math.cos(REC.hd)*stp,l[1]+Math.sin(REC.hd)*stp])}
 recLive()}
function recLive(){const $e=i=>document.getElementById(i);if(!$e('rt'))return;$e('rt').textContent=clk(REC.t);$e('rd').textContent=REC.d.toFixed(1).replace('.',',');$e('rv').textContent=REC.st==='run'?Math.round(REC.v):'0';$e('ra').textContent=REC.t>30?(REC.d/(REC.t/3600)).toFixed(1).replace('.',','):'0';$e('ru').textContent=Math.round(REC.up);$e('rl').innerHTML=recSvg(REC.pts,320,200)}
function recGo(st){REC.st=st;document.querySelector('.tabbar').classList.toggle('rec',st==='run'||st==='pause');clearInterval(REC.iv);if(st==='run')REC.iv=setInterval(recTick,1000);recUI()}
function recReset(){Object.assign(REC,{st:'idle',t:0,d:0,up:0,pts:[[0,0]],hd:Math.random()*6.28,stops:[],v:0,name:'Sortie libre'});recGo('idle')}
function recUI(){const B=$('#recb');if(!B)return;
 if(REC.st==='idle'){B.innerHTML=`<p class="sub" style="margin:0;font-size:14px">Pas de GPS ni de montre ? Ton téléphone suffit : on enregistre ta sortie, et elle apparaît dans ton historique.</p>
  <button class="rb" id="rgo" type="button">Démarrer</button><p class="rs">Appuie quand tu pars</p>
  <p class="rtip"><b>Bon à savoir :</b> garde l’appli ouverte et l’écran allumé pendant la sortie, le temps que la version native gère l’enregistrement en arrière-plan. Pense à autoriser la localisation.</p>`;$('#rgo').onclick=()=>recGo('run');return}
 if(REC.st==='done'){const km=Math.round(REC.d*10)/10;B.innerHTML=`<div class="sg"><div><b>${km.toFixed(1).replace('.',',')} km</b>distance</div><div><b>${clk(REC.t)}</b>durée</div><div><b>${Math.round(REC.up)} m</b>dénivelé</div><div><b>${REC.t>30?(REC.d/(REC.t/3600)).toFixed(1).replace('.',','):'0'} km/h</b>vitesse moyenne</div></div>
  <div class="rlive">${recSvg(REC.pts,320,200)}</div><p class="sub" style="font-size:11px;margin:4px 2px 0">Tracé de démonstration (simulé).</p>
  <label class="sub" for="rname" style="display:block;margin:12px 0 0;font-weight:600;color:var(--ink)">Nom de la sortie</label><input class="rname" id="rname" type="text" maxlength="40" value="${REC.name}">
  ${REC.stops.length?`<div class="rst"><b>Boulangeries</b><br>${REC.stops.map(s=>`${s.name} · km ${s.km.toFixed(1).replace('.',',')}`).join('<br>')}</div>`:''}
  <p class="rtip">Cette sortie te rapporte <b>${Math.round(REC.d)} XP</b> (1 km = 1 XP).</p>
  <div class="rbtn"><button type="button" id="rdel">Supprimer</button><button type="button" class="y" id="rsave">Enregistrer</button></div>`;
  $('#rname').oninput=e=>REC.name=e.target.value;$('#rdel').onclick=recReset;
  $('#rsave').onclick=()=>{const km=Math.round(REC.d*10)/10,nm=(REC.name||'Sortie libre').trim()||'Sortie libre';RIDES.unshift([new Date().toISOString().slice(0,10),nm,km,REC.t/3600,Math.round(REC.up),REC.stops.map(s=>[s.name,Math.round(s.km)])]);ME.km+=Math.round(REC.d);ME.rides++;REC.stops.forEach(s=>{if(bakOf(s.name)[6])ME.shops++});recReset();showPg('j')};return}
 const run=REC.st==='run';
 B.innerHTML=`<p class="rs" style="margin-top:4px">${run?'● Enregistrement en cours':'Sortie en pause'}</p><div class="rt" id="rt">${clk(REC.t)}</div><p class="rs">durée</p>
  <div class="rg"><div><b id="rd">0</b>km</div><div><b id="rv">0</b>km/h</div><div><b id="ra">0</b>km/h moyenne</div><div><b id="ru">0</b>m de dénivelé</div></div>
  <div class="rlive" id="rl"></div>
  <div class="rbtn"><button type="button" class="y" id="rpause">${run?'Pause':'Reprendre'}</button><button type="button" class="k" id="rend">Terminer</button></div>
  <div class="rbtn"><button type="button" id="rbak">Pause boulangerie</button></div><div id="rbox"></div>
  <p class="rtip"><label><input type="checkbox" id="racc"${REC.acc>1?' checked':''}> Démo : accélérer le temps (x60) pour voir l’enregistrement avancer</label></p>`;
 recLive();
 $('#rpause').onclick=()=>recGo(run?'pause':'run');
 $('#rend').onclick=()=>recGo('done');
 $('#racc').onchange=e=>REC.acc=e.target.checked?60:1;
 $('#rbak').onclick=()=>{const bx=$('#rbox');if(bx.innerHTML){bx.innerHTML='';return}const L=ALL.filter(b=>b[6]),O=ALL.filter(b=>!b[6]).slice(0,4);
  bx.innerHTML=`<div class="rst"><b>Où es-tu arrêté ?</b><select id="rsel">${L.map(b=>`<option>${b[0]}</option>`).join('')}${O.map(b=>`<option>${b[0]}</option>`).join('')}</select><div class="rbtn"><button type="button" class="y" id="rok">Ajouter la pause</button></div></div>`;
  $('#rok').onclick=()=>{const n=$('#rsel').value,b=bakOf(n);REC.stops.push({name:n,km:REC.d,p:REC.pts[REC.pts.length-1]});recLive();$('#rbox').innerHTML=`<div class="rst"><b>Pause ajoutée : ${n}</b><br>${b[6]?`Partenaire : ${adv(b)}.<br>Montre ton code à la boulangerie pour valider ton passage.<div class="rbtn"><button type="button" class="y" id="rqr">Ouvrir mon code</button></div>`:'Cette boulangerie n’est pas partenaire : pas de passage à valider.'}</div>`;const q=$('#rqr');if(q)q.onclick=()=>showPg('f')}}}
'''
for fn in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+fn;s=open(p,encoding='utf-8').read()
    def rep(a,b):
        global s
        assert a in s,(fn,a[:60]);s=s.replace(a,b,1)
    rep("</style>",CSS+"</style>")
    rep('<div class="ov" id="hd" hidden',REC_HTML+'<div class="ov" id="hd" hidden')
    rep('<button type="button" role="tab" data-p="f"',BTN+'<button type="button" role="tab" data-p="f"')
    rep("const m={h:'pgHome',j:'pgHist',f:'pgFid',p:'pgProf'}","const m={h:'pgHome',j:'pgHist',r:'pgRec',f:'pgFid',p:'pgProf'}")
    rep("if(p==='j')histRender();","if(p==='j')histRender();if(p==='r')recUI();")
    rep("function histRender(){",JS+"const hs=r=>[...r[0]+r[1]].reduce((a,c)=>a+c.charCodeAt(0),0)%23;\nfunction histRender(){")
    rep("loopSvg(i,r,104,104)","loopSvg(hs(r),r,104,104)")
    rep("loopSvg(i,r,320,200,pins)","loopSvg(hs(r),r,320,200,pins)")
    open(p,'w',encoding='utf-8').write(s)
print('ok')
