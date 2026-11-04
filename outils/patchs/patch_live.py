import re
for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new):
        global s
        assert s.count(old)==1,(f,old[:80],s.count(old))
        s=s.replace(old,new)
    css=r""".nxp{width:100%;border:2px solid var(--ink);border-radius:18px;padding:10px 12px;background:#fff;text-align:left}
.nxp .nxh{display:flex;justify-content:space-between;gap:8px;font:700 13px Poppins,sans-serif;margin-bottom:6px}.nxp .nxh span{color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
.nxp .xpb{margin:0 0 8px;height:12px}
.nxp .nxs{margin:0;font:500 13px/1.45 Poppins,sans-serif}.nxp .nxs.fin{font-weight:700}
.nxp .here{border:2px solid var(--ink);background:var(--yellow);border-radius:14px;padding:10px 12px;display:flex;flex-direction:column;gap:6px;font:500 13px Poppins,sans-serif;animation:xpop .5s}
.nxp .here b{font:800 15px Poppins,sans-serif}.nxp .here span{display:flex;align-items:center;gap:6px}
.nxp .here button{border:2px solid var(--ink);background:#141414;color:#fff;border-radius:99px;padding:10px;font:800 14px Poppins,sans-serif;cursor:pointer}
.nxp .nxm{margin:8px 0 0;font:700 12px Poppins,sans-serif;color:var(--ok,#1E8A4C)}
.nxp .dmo{display:block;margin-top:8px;border:0;background:transparent;color:var(--muted);font:600 11.5px Poppins,sans-serif;text-decoration:underline;cursor:pointer;padding:0}
.rbn{display:flex;flex-direction:column;gap:6px;width:100%}.rbn .bl{display:flex;align-items:center;gap:8px;border:2px solid var(--ink);border-radius:14px;background:var(--yellow);padding:8px 12px;font:600 13px Poppins,sans-serif;color:#141414;animation:xpop .5s}.rbn .bl em{margin-left:auto;font:800 13px Poppins,sans-serif;font-style:normal}
.dmsel{display:flex;align-items:center;justify-content:center;gap:8px;font:600 12px Poppins,sans-serif;color:var(--muted)}.dmsel select{border:2px solid var(--ink);border-radius:99px;padding:5px 10px;font:600 12px Poppins,sans-serif;background:#fff;color:var(--ink)}
#qrp{z-index:50;padding:14px 16px 28px}.qrbig{width:230px;max-width:70%;margin:14px auto;border:2px solid var(--ink);border-radius:18px;padding:12px;background:#fff}.qrbig svg{display:block;width:100%;height:auto}
"""
    rep(".lo{display:block;",css+".lo{display:block;")
    rep('  <div class="ov auth" id="auth"','  <div class="ov" id="qrp" hidden role="dialog" aria-label="Valider mon passage"><div class="sumh"><button class="ovx" id="qrx" type="button" aria-label="Retour">←</button><h2>Valider mon passage</h2></div><div id="qrb"></div></div>\n  <div class="ov auth" id="auth"')
    # démo : heure de départ simulée dans Profil
    rep('<div class="set"><div class="row"><span>Connecté en tant que</span>','<div class="set"><div class="row"><label for="f_dh">Démo : heure de départ</label><select id="f_dh"><option value="">Heure réelle</option><option value="6.75">6 h 45</option><option value="7.5">7 h 30</option><option value="10.25">10 h 15</option></select></div><div class="row"><span>Connecté en tant que</span>')
    # --- recStart / REC state ---
    rep("function recStart(mode){clearInterval(REC.t);Object.assign(REC,{sec:0,km:0,gain:0,stops:[],pts:[[0,0]],h:Math.random()*6.28,paused:false,mode,v:0});REC.t=setInterval(recTick,1000);recView('run')}",
r"""let DEMOH=null;try{const v=localStorage.getItem('mr_demoh');DEMOH=v?+v:null}catch(e){}
const nowH=()=>{const d=new Date();return d.getHours()+d.getMinutes()/60};
function recStart(mode){clearInterval(REC.t);const startH=DEMOH!=null?DEMOH:nowH(),P=(mode==='tracé'&&S.cur&&S.cur.P.length)?{km:S.cur.km,name:S.sumt||'Mon tracé',rmode:S.mode,stops:S.cur.P.map((b,x)=>({n:b[0],km:stopAt(x,S.cur.P.length,S.cur.km,b).km,gift:!!b[6],adv:b[6]?adv(b):''}))}:null;
 Object.assign(REC,{sec:0,km:0,gain:0,stops:[],pts:[[0,0]],h:Math.random()*6.28,paused:false,mode,v:0,startH,plan:P,msg:'',nk:'',sb:startChal(startH)});REC.t=setInterval(recTick,1000);recView('run')}
const hash=t=>{let h=7;for(const c of t)h=(h*31+c.charCodeAt(0))>>>0;return h};
function recNext(force){const e=$('#rnext');if(!e)return;const P=REC.plan;if(!P){e.innerHTML='';return}
 const done=new Set(REC.stops.map(x=>x.n)),nx=P.stops.find(x=>!done.has(x.n)),left=Math.max(0,P.km-REC.km),d=nx?nx.km-REC.km:0,st=left<=.05?'fin':nx?(d<=.3?'here':'go'):'last',key=st+'|'+(nx?nx.n:'')+'|'+REC.msg;
 const km=REC.km.toFixed(1).replace('.',','),pct=Math.min(100,REC.km/P.km*100).toFixed(1);
 const info=st==='go'?`Prochaine pause : <b>${nx.n}</b><br>dans ${d.toFixed(1).replace('.',',')} km${REC.v>1?' · environ '+Math.max(1,Math.round(d/REC.v*60))+' min':''} · encore ${left.toFixed(1).replace('.',',')} km au total`:'';
 if(force||e.dataset.k!==key){e.dataset.k=key;
  let h=`<div class="nxp"><div class="nxh"><b>${P.name}</b><span id="nxk">${km} / ${P.km} km</span></div><div class="xpb"><i id="nxb" style="width:${pct}%"></i></div>`;
  if(st==='fin')h+='<p class="nxs fin">Tracé terminé ! Touche « Terminer la sortie ».</p>';
  else if(st==='here')h+=`<div class="here"><b>Tu y es : ${nx.n}</b>${nx.gift?`<span>${GIFT} ${nx.adv}</span>`:'<span>Pas encore partenaire, mais une bonne adresse.</span>'}<button type="button" id="rvp">${nx.gift?'Valider mon passage':'Je m’arrête ici'}</button></div>`;
  else if(st==='go')h+=`<p class="nxs" id="nxi">${info}</p>`;
  else h+=`<p class="nxs" id="nxi">Plus de pause prévue : encore ${left.toFixed(1).replace('.',',')} km jusqu’à l’arrivée.</p>`;
  if(REC.msg)h+=`<p class="nxm">${REC.msg}</p>`;
  h+='<button type="button" class="dmo" id="rff">Avancer de 5 km (démo)</button></div>';e.innerHTML=h;
  const v=$('#rvp');if(v)v.onclick=()=>qrOpen(nx);const ff=$('#rff');if(ff)ff.onclick=()=>{const l=REC.pts[REC.pts.length-1];REC.km+=5;REC.sec+=5/Math.max(REC.v||25,20)*3600;REC.gain+=18;REC.pts.push([l[0]+Math.cos(REC.h)*5,l[1]+Math.sin(REC.h)*5]);recUpd()}}
 else{const a=$('#nxk');if(a)a.textContent=km+' / '+P.km+' km';const b=$('#nxb');if(b)b.style.width=pct+'%';const i=$('#nxi');if(i&&st==='go')i.innerHTML=info}}
function qrOpen(nx){const Q=$('#qrp');$('#qrb').innerHTML=nx.gift?`<p class="sub" style="margin:0">Montre ce code à <b>${nx.n}</b>. Le commerçant le scanne avec son téléphone.</p><div class="qrbig">${qrSvg(hash(nx.n)+Math.floor(Date.now()/30000))}</div><p class="sub" style="text-align:center;font-size:12px">Le code change toutes les 30 secondes (démo).</p><div class="sybtn"><button type="button" id="qrno">Annuler</button><button class="y" type="button" id="qryes">Passage validé (démo)</button></div>`:'';
 Q.hidden=false;$('#qrx').onclick=$('#qrno')?$('#qrno').onclick=()=>{Q.hidden=true}:()=>{Q.hidden=true};$('#qrx').onclick=()=>{Q.hidden=true};
 $('#qryes').onclick=()=>{Q.hidden=true;qrDone(nx)}}
function qrDone(nx){REC.stops.push({n:nx.n,km:REC.km,i:REC.pts.length-1});const L=LOY[nx.n];
 if(L){L.p++;if(L.p>=L.n){REC.msg='Passage validé ✓ · récompense : '+L.r+' !';L.p=0}else REC.msg=`Passage validé ✓ · ${L.p} sur ${L.n} pour obtenir ${L.r}`}else REC.msg='Passage enregistré ✓';
 recStopsUI();recNext(true)}
""")
    # non-partner stop: direct record
    rep("const v=$('#rvp');if(v)v.onclick=()=>qrOpen(nx);","const v=$('#rvp');if(v)v.onclick=()=>nx.gift?qrOpen(nx):qrDone(nx);")
    # run view markup: banners + panel
    rep("<div class=\"rt\" id=\"rt\">0:00:00</div><div class=\"rg\">","<div class=\"rt\" id=\"rt\">0:00:00</div>${(REC.sb||[]).length?`<div class=\"rbn\">${REC.sb.map(c=>`<div class=\"bl\"><i>✓</i><span>Défi validé au départ : <b>${c.t}</b></span><em>+${c.xp} XP</em></div>`).join('')}</div>`:''}<div id=\"rnext\" style=\"width:100%\"></div><div class=\"rg\">")
    rep("$('#rmp').innerHTML=recMap()}","$('#rmp').innerHTML=recMap();recNext()}")
    rep("recUpd();$('#rpz').onclick=()=>{REC.paused=!REC.paused;recView('run')}","recNext(true);recUpd();$('#rpz').onclick=()=>{REC.paused=!REC.paused;recView('run')}")
    # idle view : heure de départ démo
    rep("$('#rgo').onclick=()=>recStart(fol?'tracé':'libre');","{const sel=$('#rdh');if(sel){sel.value=DEMOH==null?'':String(DEMOH);sel.onchange=()=>{DEMOH=sel.value===''?null:+sel.value;try{localStorage.setItem('mr_demoh',sel.value)}catch(e){}}}}$('#rgo').onclick=()=>recStart(fol?'tracé':'libre');")
    rep("<button class=\"go\" id=\"rgo\" type=\"button\">GO</button>","<button class=\"go\" id=\"rgo\" type=\"button\">GO</button><label class=\"dmsel\">Démo · heure de départ<select id=\"rdh\"><option value=\"\">Heure réelle</option><option value=\"6.75\">6 h 45</option><option value=\"7.5\">7 h 30</option><option value=\"10.25\">10 h 15</option></select></label>")
    # done view : défis / badges
    old_done="</div></div>${xpBlock()}${REC.stops.length?"
    rep(old_done,"</div></div>${xpBlock()}${bonusHTML((REC.sb||[]),[]).replace(/Défi validé :/g,'Défi validé au départ :')}${bonusHTML(PV.claims,PV.badges)}${REC.stops.length?")
    rep("else if(v==='done'){const km=REC.km,h=REC.sec/3600,def=(REC.mode==='tracé'&&S.sumt)?S.sumt:'Sortie libre';","else if(v==='done'){const km=REC.km,h=REC.sec/3600,def=(REC.mode==='tracé'&&REC.plan&&REC.plan.name)?REC.plan.name:(REC.mode==='tracé'&&S.sumt)?S.sumt:'Sortie libre',SS=(REC.sb||[]).reduce((a,c)=>a+c.xp,0),PV=previewDone(recRide(def),SS);REC.pv=PV;")
    rep("$('#rres').onclick=()=>{cancelAnimationFrame(REC.raf);REC.paused=false;recView('run')};$('#rdel').onclick=()=>{cancelAnimationFrame(REC.raf);recReset()};xpAnim(Math.round(REC.km))}","$('#rres').onclick=()=>{cancelAnimationFrame(REC.raf);REC.paused=false;recView('run')};$('#rdel').onclick=()=>{cancelAnimationFrame(REC.raf);recReset()};xpAnim(PV.gain,'xp',PV.base)}")
    # recSave
    a=s.index("function recSave(){");b=s.index("function recReset(){")
    s=s[:a]+r"""function recRide(name){const km=Math.round(REC.km*10)/10;return [todayIso(),(name||'Sortie libre').trim(),km,REC.sec/3600,Math.round(REC.gain),REC.stops.map(x=>[x.n,Math.round(x.km*10)/10]),REC.startH,(REC.plan&&REC.plan.rmode==='train')?'train':'']}
function recSave(){const SS=(REC.sb||[]).reduce((a,c)=>a+c.xp,0);finishRide(recRide($('#rnm').value),SS);
 recReset();showPg('j')}
"""+s[b:]
    # lancer le trajet depuis l'accueil : démo heure
    # profil : select heure démo
    rep("profInit();bikeInit();","profInit();(()=>{const e=$('#f_dh');if(e){e.value=DEMOH==null?'':String(DEMOH);e.onchange=()=>{DEMOH=e.value===''?null:+e.value;try{localStorage.setItem('mr_demoh',e.value)}catch(x){}}}})();bikeInit();")
    open(p,'w',encoding='utf-8').write(s);print(f,'part2 ok')
