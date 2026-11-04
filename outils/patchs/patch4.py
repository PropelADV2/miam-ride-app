import re
CSS='''
.dvi{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:0;background:transparent;padding:11px 14px;font:inherit;color:var(--ink);cursor:pointer}.dvi+.dvi,.set .dvi+.row{border-top:2px solid var(--peach)}
.dvm{flex:none;width:38px;height:38px;border-radius:50%;border:2px solid var(--ink);background:var(--yellow);display:grid;place-items:center;font:800 15px Poppins,sans-serif}
.dvi b{display:block;font-weight:700;font-size:14px;line-height:1.2}.dvi small{display:block;color:var(--muted);font-size:12px;font-weight:500}.dvi .ok{margin-left:auto;font:800 11px Poppins,sans-serif;white-space:nowrap}.dvi .ok::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:#2E9E5B;margin-right:5px}
.dvadd{display:block;width:100%;margin-top:10px;border:2px solid var(--ink);background:var(--yellow);border-radius:99px;padding:12px;font:800 14px Poppins,sans-serif;cursor:pointer;color:var(--ink)}
#dv{z-index:40;padding:14px 16px 28px}.dvg{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:6px}.dvg button{display:flex;gap:10px;align-items:center;text-align:left;border:2px solid var(--ink);background:#fff;border-radius:16px;padding:10px;font:inherit;color:var(--ink);cursor:pointer}.dvg b{display:block;font-weight:700;font-size:13.5px;line-height:1.15}.dvg small{display:block;color:var(--muted);font-size:11px;font-weight:500;line-height:1.2}
.dvp{border:2px solid var(--ink);border-radius:16px;overflow:hidden;margin-top:10px}.dvp .row{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 14px;font-size:13.5px;font-weight:600}.dvp .row+.row{border-top:2px solid var(--peach)}
.dvok{text-align:center;padding:18px 8px}.dvok .tick{width:64px;height:64px;border-radius:50%;background:var(--yellow);border:3px solid var(--ink);display:grid;place-items:center;margin:0 auto 10px;font:800 30px Poppins,sans-serif}
.dvin{width:100%;border:2px solid var(--ink);border-radius:12px;padding:10px 12px;font:600 14px Poppins,sans-serif;margin-top:6px}
'''
SECTION='''<h2 class="st">Montres et GPS</h2>
    <div class="set" id="dvlist"></div>
    <button class="dvadd" id="dvadd" type="button">Ajouter une montre ou un GPS</button>
    <p class="sub" style="font-size:12px;margin:6px 2px 0">Pour envoyer tes tracés et récupérer tes sorties automatiquement. Démonstration : aucune connexion réelle.</p>
    '''
OV='''<div class="ov" id="dv" hidden role="dialog" aria-label="Montres et GPS"><div class="sumh"><button class="ovx" id="dvx" type="button" aria-label="Retour">←</button><h2 id="dvt">Appareil</h2></div><div id="dvb"></div></div>
  '''
JS='''
const DVB=[["Garmin","Compteur ou montre","compte"],["Wahoo","Compteur GPS","compte"],["Hammerhead","Compteur Karoo","compte"],["Strava","Application","compte"],["Polar","Montre","compte"],["Suunto","Montre","compte"],["Coros","Montre","compte"],["Apple Watch","Montre, via l’iPhone","app"]];
PROF.dev=Array.isArray(PROF.dev)?PROF.dev:[];
const ago=t=>{const m=Math.round((Date.now()-t)/60000);return m<1?'à l’instant':m<60?`il y a ${m} min`:m<1440?`il y a ${Math.round(m/60)} h`:`il y a ${Math.round(m/1440)} j`};
const sendBtns=()=>{const d=PROF.dev.filter(x=>x.send);return d.length?d.map(x=>`<button type="button" data-s="${x.m||x.b}">Envoyer à ${x.m||x.b}</button>`).join(''):'<button type="button" data-s="conn">Connecter un appareil</button>'};
function dvRender(){const L=$('#dvlist');if(!L)return;L.innerHTML=PROF.dev.length?PROF.dev.map((d,i)=>`<button type="button" class="dvi" data-i="${i}"><span class="dvm">${d.b[0]}</span><span><b>${d.m||d.b}</b><small>${d.b} · synchronisé ${ago(d.sync)}</small></span><span class="ok">Connecté</span></button>`).join(''):'<div class="row"><span style="font-weight:500;color:var(--muted)">Aucun appareil connecté pour l’instant.</span></div>';
 L.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>dvOpen('detail',+b.dataset.i))}
function dvOpen(step,arg){const B=$('#dvb'),T=$('#dvt');$('#dv').hidden=false;$('#dv').scrollTop=0;
 if(step==='pick'){T.textContent='Ajouter un appareil';B.innerHTML=`<p class="sub" style="margin:0 0 8px">Choisis la marque de ta montre ou de ton compteur GPS.</p><div class="dvg">${DVB.map((b,i)=>`<button type="button" data-b="${i}"><span class="dvm">${b[0][0]}</span><span><b>${b[0]}</b><small>${b[1]}</small></span></button>`).join('')}</div><button class="dvadd" style="background:#fff" id="dvother" type="button">Mon appareil n’est pas dans la liste</button>`;
  B.querySelectorAll('[data-b]').forEach(b=>b.onclick=()=>dvOpen('link',+b.dataset.b));$('#dvother').onclick=()=>dvOpen('manual')}
 else if(step==='manual'){T.textContent='Autre appareil';B.innerHTML=`<p class="sub" style="margin:0">Pas de connexion automatique pour cet appareil, mais tu peux quand même l’utiliser :</p><ol class="tl" style="margin-top:12px"><li><span class="pt">1</span><b>Génère ton tracé</b><small>Depuis l’accueil, choisis tes pauses.</small></li><li><span class="pt">2</span><b>Télécharge le GPX</b><small>Dans le résumé du tracé.</small></li><li><span class="pt">3</span><b>Copie-le sur ton appareil</b><small>Par câble, Bluetooth ou via l’appli de ta marque.</small></li></ol><button class="dvadd" id="dvback" type="button">Retour</button>`;$('#dvback').onclick=()=>dvOpen('pick')}
 else if(step==='link'){const b=DVB[arg],app=b[2]==='app';T.textContent=b[0];
  B.innerHTML=`<div class="me" style="background:#fff"><div class="dvm" style="width:50px;height:50px;font-size:20px">${b[0][0]}</div><div><b style="font-size:17px">${b[0]}</b><small>${b[1]}</small></div></div>
  <p class="sub" style="margin:12px 0 0">${app?'La connexion passe par l’appli Miam Ride sur ton iPhone, qui parle à ta montre.':`Tu seras redirigé vers ton compte ${b[0]} pour autoriser Miam Ride, puis tu reviens ici.`}</p>
  <h2 style="font-size:15px;margin:14px 0 0">Ce que Miam Ride pourra faire</h2><div class="dvp"><div class="row"><span>Envoyer mes tracés vers l’appareil</span><button class="tg" type="button" role="switch" aria-checked="true" id="dsend" aria-label="Envoyer mes tracés"></button></div><div class="row"><span>Récupérer mes sorties dans l’historique</span><button class="tg" type="button" role="switch" aria-checked="true" id="dget" aria-label="Récupérer mes sorties"></button></div></div>
  <label class="sub" for="dmod" style="display:block;margin:14px 0 0;font-weight:600;color:var(--ink)">Nom ou modèle (facultatif)</label><input class="dvin" id="dmod" type="text" maxlength="30" placeholder="Ex. : Edge 840, Forerunner 265">
  <button class="dvadd" id="dgo" type="button">Se connecter à ${b[0]}</button><p class="saved" id="dst"></p><p class="rtip" style="font-size:11.5px;color:var(--muted)">Démonstration : tu ne seras pas redirigé vers ${b[0]} pour de vrai. Dans la vraie version, la connexion dépend de l’accord de chaque marque (à vérifier).</p>`;
  B.querySelectorAll('.tg').forEach(t=>t.onclick=()=>t.setAttribute('aria-checked',t.getAttribute('aria-checked')!=='true'));
  $('#dgo').onclick=()=>{$('#dgo').disabled=true;$('#dst').textContent=`Connexion à ${b[0]}…`;setTimeout(()=>{const d={b:b[0],m:($('#dmod').value||'').trim(),sync:Date.now(),send:$('#dsend').getAttribute('aria-checked')==='true',get:$('#dget').getAttribute('aria-checked')==='true'};PROF.dev.push(d);persist();dvRender();
   B.innerHTML=`<div class="dvok"><div class="tick">✓</div><b style="font-size:18px">${d.m||d.b} est connecté</b><p class="sub">${d.send?'Tes tracés pourront être envoyés en un tap depuis le résumé. ':''}${d.get?'Tes sorties seront ajoutées à ton historique.':''}</p></div><button class="dvadd" id="dfin" type="button">Terminer</button>`;$('#dfin').onclick=()=>{$('#dv').hidden=true}},1200)}}
 else if(step==='detail'){const d=PROF.dev[arg];T.textContent=d.m||d.b;
  B.innerHTML=`<div class="me" style="background:#fff"><div class="dvm" style="width:50px;height:50px;font-size:20px">${d.b[0]}</div><div><b style="font-size:17px">${d.m||d.b}</b><small>${d.b} · synchronisé ${ago(d.sync)}</small></div></div>
  <div class="dvp"><div class="row"><span>Envoyer mes tracés vers l’appareil</span><button class="tg" type="button" role="switch" aria-checked="${d.send}" id="xs" aria-label="Envoyer mes tracés"></button></div><div class="row"><span>Récupérer mes sorties</span><button class="tg" type="button" role="switch" aria-checked="${d.get}" id="xg" aria-label="Récupérer mes sorties"></button></div></div>
  <div class="rbtn"><button type="button" class="y" id="xsync">Synchroniser</button><button type="button" id="xdel">Déconnecter</button></div><p class="saved" id="xst"></p>`;
  $('#xs').onclick=e=>{d.send=!d.send;e.currentTarget.setAttribute('aria-checked',String(d.send));persist()};$('#xg').onclick=e=>{d.get=!d.get;e.currentTarget.setAttribute('aria-checked',String(d.get));persist()};
  $('#xsync').onclick=()=>{d.sync=Date.now();persist();dvRender();$('#xst').textContent='✓ Synchronisé à l’instant (démo)'};
  $('#xdel').onclick=()=>{PROF.dev.splice(arg,1);persist();dvRender();$('#dv').hidden=true}}}
'''
for fn in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+fn;s=open(p,encoding='utf-8').read()
    def rep(a,b,rx=False):
        global s
        if rx:
            s,n=re.subn(a,lambda m:b,s,count=1,flags=re.S);assert n==1,(fn,a[:50])
        else:
            assert a in s,(fn,a[:60]);s=s.replace(a,b,1)
    rep("</style>",CSS+"</style>")
    rep(r'<h2 class="st">Applications connectées</h2>.*?(?=<h2 class="st">Compte</h2>)',SECTION,True)
    rep('<div class="ov" id="hd" hidden',OV+'<div class="ov" id="hd" hidden')
    rep('function openSum(){',JS+'function openSum(){')
    rep('<button type="button" data-s="Garmin">Envoyer à Garmin</button><button type="button" data-s="Wahoo">Envoyer à Wahoo</button>','${sendBtns()}')
    rep("if(k==='edit')return closeSum();","if(k==='edit')return closeSum();if(k==='conn'){closeSum();return showPg('p')}")
    rep("`Démo : envoi vers ${k} (connexion à faire dans Profil).`","`Démo : tracé envoyé vers ${k}.`")
    rep("$('#sumx').onclick=closeSum;","$('#sumx').onclick=closeSum;$('#dvx').onclick=()=>{$('#dv').hidden=true};$('#dvadd').onclick=()=>dvOpen('pick');dvRender();")
    rep("if(!$('#hd').hidden)closeRide()","if(!$('#hd').hidden)closeRide();if(!$('#dv').hidden)$('#dv').hidden=true") if "if(!$('#hd').hidden)closeRide()" in s else None
    open(p,'w',encoding='utf-8').write(s)
print('ok')
