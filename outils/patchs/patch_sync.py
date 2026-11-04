import re
for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new):
        global s
        assert s.count(old)==1,(f,old[:70],s.count(old))
        s=s.replace(old,new)
    css=r"""#sy{z-index:45;padding:14px 16px 28px}
.pl{border:2px solid var(--ink);border-radius:18px;background:#fff;margin-top:10px;padding:12px}
.pl .top{display:flex;gap:10px;align-items:center}.pl .mp{flex:none;width:64px;height:64px;border-radius:12px;overflow:hidden;border:2px solid var(--ink);background:var(--peach)}.pl .mp svg{width:100%;height:100%;display:block}
.pl b{display:block;font-weight:800;font-size:15px}.pl small{color:var(--muted);font-size:12px;display:block}
.pl .via{display:inline-block;margin-top:3px;font:700 11px Poppins,sans-serif;border:2px solid var(--ink);border-radius:99px;padding:0 8px;background:var(--peach)}
.stp{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-top:10px}
.stp span{font:700 10.5px Poppins,sans-serif;text-align:center;border:2px solid var(--ink);border-radius:99px;padding:3px 0;background:#fff;color:var(--muted)}
.stp span.ok{background:var(--yellow);color:var(--ink)}.stp span.now{background:var(--ink);color:#fff}.stp span.bad{background:#FFE9E5;border-color:#b3261e;color:#b3261e}
.pl .act{display:flex;gap:8px;margin-top:10px}.pl .act button,.plimp{flex:1;border:2px solid var(--ink);border-radius:99px;padding:9px;font:700 13px Poppins,sans-serif;cursor:pointer;background:#fff;color:var(--ink)}.pl .act button.y{background:var(--yellow)}
.plimp{display:block;width:100%;margin-top:10px;flex:none}
.plxp{font:800 13px Poppins,sans-serif;margin-top:8px}
.syl{list-style:none;margin:12px 0 0;padding:0;display:flex;flex-direction:column;gap:8px}
.syl li{display:flex;gap:10px;align-items:flex-start;border:2px solid var(--ink);border-radius:14px;padding:9px 12px;background:#fff;font-weight:600;font-size:13px;animation:xpop .5s}
.syl li i{flex:none;width:22px;height:22px;border-radius:50%;border:2px solid var(--ink);background:var(--yellow);display:flex;align-items:center;justify-content:center;font-style:normal;font-size:12px;font-weight:800}
.syl li.no i{background:#FFE9E5;border-color:#b3261e;color:#b3261e}.syl li small{display:block;color:var(--muted);font-weight:500}
.mt{height:16px;border:2px solid var(--ink);border-radius:99px;background:#fff;position:relative;overflow:hidden;margin-top:6px}.mt i{display:block;height:100%;width:0;background:var(--yellow);transition:width 1.6s cubic-bezier(.2,.7,.2,1)}.mt i.no{background:#f4a8a0}
.mt u{position:absolute;left:80%;top:0;bottom:0;border-left:2px dashed var(--ink)}
.cmp svg{display:block;width:100%;height:auto;background:var(--peach);border-radius:14px}
.cmp .lg{display:flex;gap:14px;font:600 11px Poppins,sans-serif;color:var(--muted);margin-top:6px}
.sybtn{display:flex;gap:8px;margin-top:12px}.sybtn button{flex:1;border:2px solid var(--ink);border-radius:99px;padding:11px;font:800 14px Poppins,sans-serif;cursor:pointer;background:#fff;color:var(--ink)}.sybtn button.y{background:var(--yellow)}
"""
    rep(".lo{display:block;",css+".lo{display:block;")
    rep('<div class="hs" id="hsum"></div>','<div id="hplan"></div>\n    <div class="hs" id="hsum"></div>')
    rep('  <div class="ov auth" id="auth"','  <div class="ov" id="sy" hidden role="dialog" aria-label="Synchro de ta sortie"><div class="sumh"><button class="ovx" id="syx" type="button" aria-label="Retour">←</button><h2>Synchro de ta sortie</h2></div><div id="syb"></div></div>\n  <div class="ov auth" id="auth"')
    # generalise xp block
    i=s.index("function xpBlock(){");j=s.index("function recStart(mode){")
    new=r"""function xpBlock(p){p=p||'xp';return `<div class="xpc"><div class="xph"><span>XP gagnée</span><b id="${p}g">+0</b></div><div class="xpr"><div class="xpbk" id="${p}bk"></div><div class="xpb big" id="${p}bar" role="img" aria-label="Progression vers le prochain vélo"><i id="${p}f" style="width:0"></i></div></div><div class="xpl"><span id="${p}l1"></span><span id="${p}l2"></span></div><p class="nx" id="${p}n"></p><div class="xpup" id="${p}u" hidden></div></div>`}
function xpAnim(gain,p){p=p||'xp';cancelAnimationFrame(REC.raf);const f=$('#'+p+'f');if(!f)return;
 gain=Math.max(1,gain==null?Math.round(REC.km):gain);const x0=XPOF(),x1=x0+gain,g=$('#'+p+'g'),l1=$('#'+p+'l1'),l2=$('#'+p+'l2'),nn=$('#'+p+'n'),u=$('#'+p+'u'),bk=$('#'+p+'bk'),bar=$('#'+p+'bar');
 let lv=-1;const setLv=xp=>{const L=lvOf(xp),n=BIKES[L+1];if(L===lv)return;const up=lv>=0;lv=L;l1.textContent=BIKES[L][0]+' '+BIKES[L][1];l2.textContent=n?n[3].toLocaleString('fr-FR')+' XP':'Max';bk.innerHTML=bikeSvg(L,false).replace('width="64" height="38"','width="64" height="38" style="display:block;max-width:100%"');
  if(up){u.hidden=false;u.textContent='Nouveau vélo débloqué : '+BIKES[L][0]+' '+BIKES[L][1]+' !';bk.classList.remove('pop');void bk.offsetWidth;bk.classList.add('pop')}};
 const end=()=>{const n=BIKES[lvOf(x1)+1];bar.classList.add('done');nn.textContent=n?`Encore ${(n[3]-x1).toLocaleString('fr-FR')} XP avant ${n[0]} ${n[1]}.`:'Tu as le meilleur vélo du garage !'};
 const frame=xp=>{setLv(xp);f.style.width=pctAt(xp).toFixed(2)+'%'};
 frame(x0);
 if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){frame(x1);g.textContent='+'+gain+' XP';end();return}
 const T=Math.min(3600,1400+gain*8),t0=performance.now()+450;
 const step=now=>{const k=Math.max(0,Math.min(1,(now-t0)/T)),e=1-Math.pow(1-k,3),xp=x0+gain*e;frame(xp);g.textContent='+'+Math.round(gain*e)+' XP';
  if(k<1)REC.raf=requestAnimationFrame(step);else{frame(x1);g.textContent='+'+gain+' XP';end()}};
 REC.raf=requestAnimationFrame(step)}
"""
    s=s[:i]+new+s[j:]
    rep("$('#rdel').onclick=()=>{cancelAnimationFrame(REC.raf);recReset()};xpAnim()}","$('#rdel').onclick=()=>{cancelAnimationFrame(REC.raf);recReset()};xpAnim(Math.round(REC.km))}")
    js=r"""
const PLAT={Garmin:'Garmin Connect',Wahoo:'Wahoo',Strava:'Strava',COROS:'COROS',Coros:'COROS',Suunto:'Suunto',Polar:'Polar Flow',Hammerhead:'Hammerhead Dashboard'};
const platOf=via=>{const d=(PROF.dev||[]).find(x=>(x.m||x.b)===via||x.b===via);return d?(PLAT[d.b]||d.b):(PLAT[via]||'ta plateforme')};
let PLANS=(()=>{try{const a=JSON.parse(localStorage.getItem('mr_plans')||'null');if(Array.isArray(a))return a}catch(e){}return[{id:1,name:'Boucle du dimanche',km:64,via:'Garmin',st:'sent',stops:[['Boulangerie Dupain',31]]}]})();
const savePlans=()=>{try{localStorage.setItem('mr_plans',JSON.stringify(PLANS.slice(0,20)))}catch(e){}};
function addPlan(k){const c=S.cur;if(!c)return;const via=k==='gpx'?'GPX':k==='share'?'Partage':k;PLANS.unshift({id:Date.now(),name:S.sumt||'Boucle',km:c.km,via,st:'sent',stops:c.P.map((b,x)=>[b[0],stopAt(x,c.P.length,c.km,b).km])});savePlans();planRender()}
function planRender(){const H=$('#hplan');if(!H)return;
 const lab=['Prévu','Envoyé','Sortie détectée','Validée'];
 let h=`<h2 class="hm" style="margin-top:10px">Tracés à rouler</h2><p class="sub" style="font-size:12px;margin:4px 0 0">Ta montre envoie la sortie à la fin du parcours : Miam Ride la compare au tracé et la valide.</p>`;
 PLANS.slice(0,4).forEach((q,i)=>{const n=q.st==='sent'?2:q.st==='check'?3:4;
  const st=lab.map((t,k)=>`<span class="${q.st==='check'&&k===2?'bad':k<n-(q.st==='sent'?1:0)?'ok':k===n-1&&q.st==='sent'?'now':''}">${k===2&&q.st==='check'?'À vérifier':t}</span>`).join('');
  const act=q.st==='sent'?`<button class="y" type="button" data-sy="${i}" data-m="ok">Simuler la synchro de ma montre</button>`:q.st==='check'?`<button type="button" data-sy="${i}" data-m="bad">Voir l’analyse</button><button class="y" type="button" data-sy="${i}" data-m="ok">Refaire la synchro</button>`:`<p class="plxp">Sortie validée · +${Math.max(1,Math.round(q.km))} XP</p>`;
  h+=`<div class="pl"><div class="top"><span class="mp">${loopSvg(i+3,null,64,64)}</span><span><b>${q.name}</b><small>${q.km} km${q.stops&&q.stops.length?' · '+q.stops.map(x=>x[0]).join(', '):''}</small><span class="via">Envoyé à ${q.via}</span></span></div><div class="stp">${st}</div><div class="${q.st==='done'?'':'act'}">${act}</div></div>`});
 h+=`<button class="plimp" type="button" id="plimp">Importer un fichier de sortie (GPX, FIT)</button><input type="file" id="plfile" accept=".gpx,.fit,.tcx" hidden>`;
 H.innerHTML=h;
 H.querySelectorAll('[data-sy]').forEach(b=>b.onclick=()=>openSync(+b.dataset.sy,b.dataset.m));
 $('#plimp').onclick=()=>$('#plfile').click();
 $('#plfile').onchange=e=>{if(!e.target.files.length)return;let i=PLANS.findIndex(q=>q.st!=='done');if(i<0){PLANS.unshift({id:Date.now(),name:'Sortie importée',km:42,via:'Fichier',st:'sent',stops:[]});i=0}e.target.value='';openSync(i,'ok',true)}}
let SYT=[];
function syClear(){SYT.forEach(clearTimeout);SYT=[];cancelAnimationFrame(REC.raf)}
function openSync(i,mode,imp){syClear();const q=PLANS[i];if(!q)return;const ok=mode==='ok',pct=ok?94:61,plat=imp?'ton fichier':platOf(q.via),km=Math.max(1,Math.round(q.km*(ok?1.02:.93)*10)/10),dur=fmtH(km/(PROF.speed||25));
 const N=70,pl=[],rd=[];for(let k=0;k<=N;k++){const t=k/N*6.2832,x=150+112*Math.cos(t)*(1+.14*Math.sin(3*t)),y=95+68*Math.sin(t);pl.push([x,y]);const dv=(!ok&&t>2.3&&t<4.1)?Math.sin((t-2.3)/1.8*3.1416)*52:0;rd.push([x+Math.sin(k*1.7)*2.2+dv*.5,y+Math.cos(k*1.3)*2.2+dv])}
 const pth=a=>'M'+a.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L'),bi=Math.round(N*.3),bp=pl[bi];
 const stop=q.stops&&q.stops[0];
 $('#syb').innerHTML=`<div class="cmp"><svg viewBox="0 0 300 190" role="img" aria-label="Comparaison entre le tracé prévu et ta sortie"><path d="M0 38H300M0 76H300M0 114H300M0 152H300M60 0V190M120 0V190M180 0V190M240 0V190" stroke="#fff" stroke-width="4"/><path d="${pth(pl)}" fill="none" stroke="#141414" stroke-opacity=".35" stroke-width="5" stroke-dasharray="2 9" stroke-linecap="round"/><path id="syr" d="${pth(rd)}" fill="none" stroke="${ok?'#141414':'#b3261e'}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="${pl[0][0].toFixed(1)}" cy="${pl[0][1].toFixed(1)}" r="6" fill="#141414" stroke="#fff" stroke-width="2"/>${stop&&ok?`<circle cx="${bp[0].toFixed(1)}" cy="${bp[1].toFixed(1)}" r="8" fill="#FFD21F" stroke="#141414" stroke-width="2.5"/>`:''}</svg><div class="lg"><span>⋯ Tracé prévu</span><span>— Ta sortie</span></div></div><ul class="syl" id="syl"></ul><div id="syx2"></div>`;
 const L=$('#syl'),add=(t,sm,bad)=>{const li=document.createElement('li');if(bad)li.className='no';li.innerHTML=`<i>${bad?'!':'✓'}</i><span>${t}${sm?`<small>${sm}</small>`:''}</span>`;L.append(li)};
 const r=$('#syr'),len=r.getTotalLength?r.getTotalLength():0;if(len){r.style.strokeDasharray=len;r.style.strokeDashoffset=len;r.getBoundingClientRect();r.style.transition='stroke-dashoffset 2.4s ease-in-out';requestAnimationFrame(()=>r.style.strokeDashoffset=0)}
 const at=(ms,fn)=>SYT.push(setTimeout(fn,ms));
 at(600,()=>add(`${plat} a reçu ta sortie`,'Ta montre s’est synchronisée à la fin du parcours.'));
 at(1500,()=>{add(`Sortie détectée : ${km} km · ${dur}`,q.name);q.st='sent'});
 at(2600,()=>{add(`Comparaison avec ton tracé`,`<span class="mt"><i id="symt"></i><u></u></span>`);const m=$('#symt');if(m){m.className=ok?'':'no';requestAnimationFrame(()=>m.style.width=pct+'%')}});
 at(4300,()=>{const li=L.lastElementChild;li.querySelector('small').innerHTML=`<b style="color:var(--ink)">${pct} % du tracé suivi</b> (seuil : 80 %)`+li.querySelector('small').innerHTML});
 if(ok){
  at(5000,()=>add(stop?`Passage à ${stop[0]}`:'Parcours terminé',stop?`Détecté vers le km ${stop[1]}`:'Arrivée détectée'));
  at(5900,()=>{add('Sortie validée','L’XP est ajoutée à ton garage.');q.st='done';savePlans();
   const d=new Date(),iso=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
   const rr=[iso,q.name,km,km/(PROF.speed||25),Math.round(km*7),(q.stops||[]).map(x=>[x[0],x[1]])];
   const xpBefore=XPOF();$('#syx2').innerHTML=xpBlock('sy')+`<div class="sybtn"><button class="y" type="button" id="syok">Voir mon historique</button></div>`;
   const gain=Math.max(1,Math.round(km));xpAnim(gain,'sy');
   RIDES.unshift(rr);ME.km+=Math.round(km);ME.rides++;try{const sv=JSON.parse(localStorage.getItem('mr_rides')||'[]');sv.unshift(rr);localStorage.setItem('mr_rides',JSON.stringify(sv.slice(0,50)))}catch(e){}
   $('#syok').onclick=()=>{$('#sy').hidden=true;histRender()};histRender()})
 }else{
  at(5000,()=>{add('À vérifier','Ta trace suit seulement 61 % du tracé prévu. Tu as peut-être pris un autre chemin : la sortie n’est pas validée automatiquement.',true);q.st='check';savePlans();
   $('#syx2').innerHTML=`<div class="sybtn"><button type="button" id="syfile">Importer un fichier</button><button class="y" type="button" id="syok">Fermer</button></div>`;
   $('#syok').onclick=()=>{$('#sy').hidden=true;histRender()};$('#syfile').onclick=()=>{$('#sy').hidden=true;histRender();$('#plimp').click()};histRender()})}
 $('#sy').hidden=false;$('#sy').scrollTop=0;$('#syx').onclick=()=>{syClear();$('#sy').hidden=true;histRender()}}
"""
    rep("function openSum(){",js+"function openSum(){")
    # hook histRender
    rep("function histRender(){","function histRender(){planRender();")
    # send handler
    old="n.textContent=k==='gpx'?'Démo : le fichier GPX sera généré ici.':k==='share'?'Démo : le partage du tracé se fera ici.':`Démo : tracé envoyé vers ${k}.`"
    rep(old,"addPlan(k);n.textContent=(k==='gpx'?'Démo : le fichier GPX serait généré et ':k==='share'?'Démo : le partage serait lancé et ':`Démo : tracé envoyé à ${k} et `)+'ajouté à Historique › Tracés à rouler.'")
    open(p,'w',encoding='utf-8').write(s);print(f,'ok')
