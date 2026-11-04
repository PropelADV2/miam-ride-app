import re,sys
fn_list=['accueil-velo.html','miam-ride-osm.html']

CSS='''
.sumbtn{display:block;width:100%;margin:0 0 8px;border:2px solid var(--ink);background:var(--ink);color:#fff;border-radius:99px;padding:12px;font:800 14px Poppins,sans-serif;cursor:pointer}.sumbtn:disabled{background:#fff;color:var(--muted);border-style:dashed;border-color:#A9A096;cursor:not-allowed}
.ambinfo{font-size:12px;color:var(--muted);margin:6px 0 0;font-weight:500}
#sum{z-index:40;padding:14px 16px 28px}.sumh{display:flex;align-items:center;gap:12px;margin-bottom:12px}.sumh h2{margin:0;font-size:20px;text-transform:uppercase;line-height:1.1}.sumh small{display:block;font:500 12px Poppins,sans-serif;color:var(--muted);text-transform:none}
.sg{display:grid;grid-template-columns:1fr 1fr;gap:8px}.sg div{border:2px solid var(--ink);border-radius:16px;padding:10px 12px;font-size:12px;font-weight:600}.sg b{display:block;font:800 20px Poppins,sans-serif}
.el{border:2px solid var(--ink);border-radius:16px;padding:10px;margin-top:8px;background:var(--peach)}.el svg{display:block;width:100%;height:auto}.el small{font-size:11.5px;color:var(--muted)}
.tl{list-style:none;margin:8px 0 0;padding:0}.tl li{position:relative;padding:0 0 14px 34px;font-size:13.5px}.tl li::before{content:"";position:absolute;left:10px;top:22px;bottom:-2px;width:2px;background:var(--ink)}.tl li:last-child::before{display:none}
.tl .pt{position:absolute;left:0;top:0;width:22px;height:22px;border-radius:50%;border:2px solid var(--ink);background:var(--yellow);display:grid;place-items:center;font:800 11px Poppins,sans-serif}.tl .pt.k{background:var(--ink);color:#fff}
.tl b{font-weight:700}.tl small{display:block;color:var(--muted);font-size:12px}.tl .gift{display:flex;gap:6px;align-items:center;font-size:12.5px;font-weight:600;margin-top:4px}
.sum2{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.sum2 button{flex:1 1 40%;border:2px solid var(--ink);background:#fff;border-radius:99px;padding:10px;font:700 13px Poppins,sans-serif;cursor:pointer;color:var(--ink)}.sum2 button.p{background:var(--yellow);flex-basis:100%}
.snote{font-size:12px;color:var(--muted);margin:8px 0 0;min-height:18px}
.set .row input[type=text],.set .row input[type=email],.set .row input[type=tel],.set .row input[type=date],.set .row input[type=number]{border:2px solid var(--ink);border-radius:12px;padding:6px 8px;font:600 13px Poppins,sans-serif;background:#fff;width:58%;min-width:0;text-align:right}
.set .row label{flex:none}.saved{font-size:12px;color:var(--muted);text-align:center;margin:10px 0 0;min-height:18px}
.warn2{background:var(--peach);border:2px solid var(--ink);border-radius:14px;padding:8px 12px;font-size:12px;margin-top:8px}
.cx{border:2px solid var(--ink);background:#fff;border-radius:99px;padding:5px 12px;font:700 12px Poppins,sans-serif;cursor:pointer;color:var(--ink)}.cx.on{background:var(--yellow)}
'''

def ro(label,inner):return f'<div class="row"><label for="{label[0]}">{label[1]}</label>{inner}</div>'
def inp(i,l,t='text',ph='',unit=''):return ro((i,l),f'<input type="{t}" id="{i}" data-f="{i}" placeholder="{ph}" autocomplete="off">')
def sel(i,l,opts,d=None):return ro((i,l),f'<select id="{i}" data-f="{i}">'+''.join(f'<option{" selected" if o==d else ""}>{o}</option>' for o in opts)+'</select>')
def tg(i,l,on):return f'<div class="row"><span>{l}</span><button class="tg" type="button" role="switch" aria-checked="{"true" if on else "false"}" aria-label="{l}" data-tg="{i}"></button></div>'
def cn(i,l,state):return f'<div class="row"><span>{l}</span><button class="cx{" on" if state else ""}" type="button" data-cx="{i}">{"Connecté" if state else "Connecter"}</button></div>'
def sec(t,body,note=''):return f'<h2 class="st">{t}</h2>\n    <div class="set">{body}</div>'+(f'\n    <p class="sub" style="font-size:12px;margin:6px 2px 0">{note}</p>' if note else '')+'\n    '
BLOOD=['Je ne sais pas','A+','A−','B+','B−','AB+','AB−','O+','O−']
PROF_HTML='''<div class="pg pgs" id="pgProf" hidden>
    <h1>Profil</h1>
    <div class="me"><div class="av" id="avt">C</div><div><b id="meName">Cycliste démo</b><small id="meLv"></small></div></div>
    <div class="src"><div><b id="mK"></b>parcourus</div><div><b id="mR"></b>sorties</div><div><b id="mS"></b>boulangeries</div></div>
    '''+sec('Mes informations',inp('f_pre','Prénom','text','Camille')+inp('f_nom','Nom','text','Martin')+inp('f_mail','E-mail','email','camille@exemple.fr')+inp('f_tel','Téléphone','tel','06 12 34 56 78')+inp('f_nai','Naissance','date')+sel('f_sex','Genre',['Non précisé','Femme','Homme','Autre'])+inp('f_ville','Ville','text','Rambouillet'))+sec('Santé et urgence',sel('f_gs','Groupe sanguin',BLOOD)+inp('f_all','Allergies','text','Ex. : pénicilline')+inp('f_med','Traitement','text','Ex. : aucun')+inp('f_cu','Contact d’urgence','text','Nom')+inp('f_cut','Tél. du contact','tel','06 98 76 54 32'),'Ces données de santé sont facultatives et sensibles : dans la vraie version, elles ne seront utilisées qu’avec ton accord explicite et ne seront partagées avec personne sans ta permission.')+sec('Mon vélo',sel('f_vt','Type',['Vélo de route','Gravel','Vélo électrique'])+inp('f_vm','Marque','text','Ex. : Giant')+inp('f_vmo','Modèle','text','Ex. : TCR Advanced')+inp('f_vp','Poids (kg)','number','8,5')+inp('f_van','Année','number','2023'),'Ton vélo réel. Il sert pour les itinéraires ; le « garage » de l’onglet Fidélité est un jeu à part.')+sec('Mon corps et ma forme',inp('f_tai','Taille (cm)','number','175')+inp('f_poi','Poids (kg)','number','70')+inp('f_fc','FC max (bpm)','number','185')+inp('f_ftp','FTP (watts)','number','230')+sel('pa','Allure moyenne',['20 km/h','25 km/h','30 km/h'],'25 km/h'),'Facultatif. L’allure moyenne sert à estimer la durée de tes sorties.')+sec('Mes préférences de route',sel('pd','Ambiance par défaut',['Routes très calmes','Calmes, avec quelques axes','Le plus direct'],'Calmes, avec quelques axes')+sel('f_un','Unités',['Kilomètres','Miles'])+tg('pav','Éviter les pavés',True))+sec('Notifications',tg('n1','Rappel avant l’expiration d’une récompense',True)+tg('n2','Nouveaux défis du mois',True)+tg('n3','Offres des boulangeries partenaires',False))+sec('Applications connectées',cn('strava','Strava',False)+cn('garmin','Garmin Connect',False)+cn('wahoo','Wahoo',False),'Démonstration : aucune connexion réelle.')+sec('Confidentialité',tg('pv1','Partager mes sorties avec mes amis',False)+tg('pv2','Apparaître dans le classement',True))+sec('Compte','<div class="row"><span>Mot de passe</span><span class="v">Modifier ›</span></div><div class="row"><span>Aide et contact</span><span class="v">›</span></div><div class="row"><span>Supprimer mon compte</span><span class="v">›</span></div>')+'''<button class="lo" type="button">Se déconnecter</button>
    <p class="saved" id="saved"></p>
    <p class="sub" style="text-align:center;font-size:11px;margin:4px 0 0">Écran de démonstration, données fictives.</p>
  </div>
  '''

SUM_HTML='''<div class="ov" id="sum" hidden role="dialog" aria-label="Résumé du tracé">
    <div class="sumh"><button class="ovx" id="sumx" type="button" aria-label="Retour">←</button><h2 id="sumt">Résumé<small id="sums"></small></h2></div>
    <div id="sumb"></div>
  </div>
  '''

JS='''
const AMB=[{n:'Routes très calmes',c:0,t:.96,r:1.04,i:'Petites routes d’abord · détour max +20 % · au moins 85 % de routes calmes'},{n:'Calmes, avec quelques axes',c:22,t:1,r:1,i:'Compromis · détour max +10 % · au moins 65 % de routes calmes'},{n:'Le plus direct',c:42,t:1.04,r:.96,i:'Itinéraire efficace · pas de détour · au moins 45 % de routes calmes'}];
const PROF={amb:1,speed:25,f:{},tg:{},cx:{}};
try{const o=JSON.parse(localStorage.getItem('mr_prof')||'null');if(o&&typeof o==='object'){Object.assign(PROF,o)}}catch(e){}
const persist=()=>{try{localStorage.setItem('mr_prof',JSON.stringify(PROF))}catch(e){}const s=$('#saved');if(s){s.textContent='✓ Enregistré sur cet appareil';clearTimeout(persist.t);persist.t=setTimeout(()=>s.textContent='',1800)}};
function ambSync(from){const i=AMB.findIndex(a=>a.n===(from==='pd'?$('#pd').value:$('#calm').value));if(i<0)return;PROF.amb=i;$('#calm').value=$('#pd').value=AMB[i].n;$('#ambinfo').textContent=AMB[i].i;if(typeof upd==='function')upd();if(S.gen)showRes()}
function spdSync(){PROF.speed=parseInt($('#pa').value)||25;upd();if(S.gen)showRes()}
function profInit(){
 const f=PROF.f;document.querySelectorAll('[data-f]').forEach(e=>{if(f[e.dataset.f]!==undefined)e.value=f[e.dataset.f];const h=()=>{f[e.dataset.f]=e.value;persist();nameUp()};e.addEventListener('change',h);e.addEventListener('input',()=>{f[e.dataset.f]=e.value;nameUp()})});
 if(PROF.f.pd)PROF.amb=Math.max(0,AMB.findIndex(a=>a.n===PROF.f.pd));if(PROF.f.pa)PROF.speed=parseInt(PROF.f.pa)||25;
 $('#pd').value=AMB[PROF.amb].n;$('#calm').value=AMB[PROF.amb].n;$('#pa').value=PROF.speed+' km/h';$('#ambinfo').textContent=AMB[PROF.amb].i;
 $('#pd').addEventListener('change',()=>ambSync('pd'));$('#calm').addEventListener('change',()=>{$('#pd').value=$('#calm').value;PROF.f.pd=$('#calm').value;persist();ambSync('calm')});$('#pa').addEventListener('change',spdSync);
 document.querySelectorAll('[data-tg]').forEach(t=>{const k=t.dataset.tg;if(PROF.tg[k]!==undefined)t.setAttribute('aria-checked',String(PROF.tg[k]));t.onclick=()=>{const v=t.getAttribute('aria-checked')!=='true';t.setAttribute('aria-checked',String(v));PROF.tg[k]=v;persist()}});
 document.querySelectorAll('[data-cx]').forEach(b=>{const k=b.dataset.cx,paint=()=>{const on=!!PROF.cx[k];b.classList.toggle('on',on);b.textContent=on?'Connecté':'Connecter'};paint();b.onclick=()=>{PROF.cx[k]=!PROF.cx[k];paint();persist()}});
 nameUp()}
function nameUp(){const p=(PROF.f.f_pre||'').trim(),n=(PROF.f.f_nom||'').trim(),full=(p+' '+n).trim()||'Cycliste démo';if($('#meName'))$('#meName').textContent=full;if($('#avt'))$('#avt').textContent=(full[0]||'C').toUpperCase()}
const fmtH=h=>{let m=Math.round(h*60);return `${Math.floor(m/60)} h ${String(m%60).padStart(2,'0')}`};
const fmtC=h=>{const m=Math.round(h*60)%1440;return `${Math.floor(m/60)} h ${String(m%60).padStart(2,'0')}`};
function elevSvg(c,dn){const W=300,H=70,N=64,ri=c.ri;let ys=[];for(let i=0;i<=N;i++){const x=i/N;ys.push(.5*Math.sin(x*(5.5+ri%3)+ri)+.32*Math.sin(x*13+ri*2)+.18*Math.sin(x*27+ri))}
 const lo=Math.min(...ys),hi=Math.max(...ys),pts=ys.map((y,i)=>[i/N*W,H-8-(y-lo)/(hi-lo)*(H-22)]);
 const d='M'+pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L');
 const mk=c.P.map((b,x)=>{const sa=stopAt(x,c.P.length,c.km,b),px=sa.pct/100*W,py=pts[Math.round(sa.pct/100*N)][1];return `<line x1="${px}" x2="${px}" y1="${py}" y2="${H}" stroke="#141414" stroke-width="1.5" stroke-dasharray="3 3"/><circle cx="${px}" cy="${py}" r="6" fill="#FFD21F" stroke="#141414" stroke-width="2"/><text x="${px}" y="${py+3.2}" text-anchor="middle" font-size="8" font-weight="800">${x+1}</text>`}).join('');
 return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Profil altimétrique de démonstration"><path d="${d} L${W} ${H} L0 ${H}Z" fill="#fff" stroke="none"/><path d="${d}" fill="none" stroke="#141414" stroke-width="2.4" stroke-linejoin="round"/>${mk}</svg>`}
function sumHTML(){const c=S.cur,a=AMB[PROF.amb],v=PROF.speed*a.t,ride=c.km/v,pauses=c.P.length*20/60,tot=ride+pauses,dn=Math.round(c.km*7.5*DEN[c.ri]*a.r),calm=Math.min(99,CALM[c.ri]-a.c),start=9;
 const MN={boucle:'Boucle',dest:'Vers un lieu',train:'Ride and train',mamie:'Laisse Mamie choisir'};S.sumt=(S.mode==='dest'&&S.fast)?'Le plus rapide':MN[S.mode];
 const from=($('#from').value||'Ma position').trim()||'Ma position';
 let steps=`<li><span class="pt k">D</span><b>Départ</b> · ${from}<small>${fmtC(start)} (heure d’exemple) · km 0</small></li>`,t=start,last=0;
 c.P.forEach((b,x)=>{const sa=stopAt(x,c.P.length,c.km,b);t+=(sa.km-last)/v+(x?20/60:0);last=sa.km;const L=LOY[b[0]];
  steps+=`<li><span class="pt">${x+1}</span><b>${b[0]}</b> · ${note(b)}<small>Arrivée vers ${fmtC(t)} · km ${sa.km} · pause conseillée : 20 min</small>${b[6]?`<span class="gift">${GIFT}<span>${adv(b)}</span></span>${L?`<small>Ton passage compte : ${L.p+1} sur ${L.n} pour obtenir ${L.r}</small>`:''}`:'<small>Pas encore partenaire : pas d’avantage, mais une bonne adresse.</small>'}</li>`});
 t+=(c.km-last)/v+(c.P.length?20/60:0);
 steps+=`<li><span class="pt k">A</span><b>${S.mode==='train'?'Arrivée · '+G()[0]:'Arrivée'}</b><small>${S.mode==='train'?G()[2]+' · ':''}vers ${fmtC(t)} · km ${c.km}</small></li>`;
 return `<div class="sg"><div><b>${c.km} km</b>distance</div><div><b>${fmtH(tot)}</b>durée avec pauses</div><div><b>${dn} m</b>dénivelé</div><div><b>${calm} %</b>routes calmes</div></div>
 <div class="el"><small>Profil du parcours (exemple)</small>${elevSvg(c,dn)}</div>
 <p class="warn2"><b>${a.n}</b> · allure ${Math.round(v)} km/h${$('#f_vm')&&($('#f_vm').value||$('#f_vmo').value)?' · '+[$('#f_vm').value,$('#f_vmo').value].filter(Boolean).join(' '):''}<br>Roulé : ${fmtH(ride)} · pauses : ${c.P.length} × 20 min</p>
 <ol class="tl">${steps}</ol>
 <div class="sum2"><button class="p" type="button" data-s="gpx">Télécharger le GPX</button><button type="button" data-s="Garmin">Envoyer à Garmin</button><button type="button" data-s="Wahoo">Envoyer à Wahoo</button><button type="button" data-s="share">Partager</button><button type="button" data-s="edit">Modifier</button></div><p class="snote" id="snote"></p>`}
function openSum(){if(!S.cur)return;$('#sumb').innerHTML=sumHTML();$('#sumt').firstChild.textContent=S.sumt+' ';$('#sums').textContent=`${S.cur.km} km · ${S.cur.P.length} pause${S.cur.P.length>1?'s':''}`;$('#sum').hidden=false;$('#sum').scrollTop=0;
 $('#sumb').querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>{const k=b.dataset.s,n=$('#snote');if(k==='edit')return closeSum();n.textContent=k==='gpx'?'Démo : le fichier GPX sera généré ici.':k==='share'?'Démo : le partage du tracé se fera ici.':`Démo : envoi vers ${k} (connexion à faire dans Profil).`});$('#sumx').focus()}
function closeSum(){$('#sum').hidden=true}
'''

for fn in fn_list:
    p='/mnt/user-data/outputs/'+fn;s=open(p,encoding='utf-8').read()
    def rep(a,b,rx=False):
        global s
        if rx:
            s,n=re.subn(a,lambda m:b,s,count=1,flags=re.S);assert n==1,(fn,a[:60])
        else:
            assert a in s,(fn,a[:60]);s=s.replace(a,b,1)
    rep("</style>",CSS+"</style>")
    # ambiance info
    rep('<option>Le plus direct</option></select></div>\n      \n    </div>','<option>Le plus direct</option></select></div>\n      <p class="ambinfo" id="ambinfo"></p>\n    </div>') if '<option>Le plus direct</option></select></div>\n      \n    </div>' in s else rep('<option>Le plus direct</option></select></div>','<option>Le plus direct</option></select></div>\n      <p class="ambinfo" id="ambinfo"></p>')
    # summary button
    rep('<div class="dl">','<button class="sumbtn" id="sumbtn" type="button" disabled>Voir le résumé du tracé</button>\n      <div class="dl">')
    # profile block
    rep(r'<div class="pg pgs" id="pgProf" hidden>.*?(?=<nav class="tabbar")',PROF_HTML+SUM_HTML,True)
    # remove old profFill+toggles
    rep(r"const toggles=\(\)=>[^\n]*\n",'',True)
    rep(r"function profFill\(\)\{[^\n]*\n",JS+"function profFill(){const xp=XPOF();let L=0;LEVELS.forEach((l,i)=>{if(xp>=l[1])L=i});$('#meLv').textContent=`Vélo ${L+1}/${BIKES.length} · ${LEVELS[L][0]} · ${xp.toLocaleString('fr-FR')} XP`;$('#mK').textContent=ME.km.toLocaleString('fr-FR')+' km';$('#mR').textContent=ME.rides;$('#mS').textContent=ME.shops}\n",True)
    # upd
    rep(r"function upd\(\)\{[^\n]*\n","function upd(){const a=AMB[PROF.amb],v=PROF.speed*a.t;$('#kv').textContent=S.km;$('#dur').textContent='environ '+(S.km/v).toFixed(1).replace('.',',')+' h à '+Math.round(v)+' km/h';syncP()}\n",True)
    # stats + cur
    rep("S.sel=ri;","S.sel=ri;S.cur={km,ri,P,D,dk};{const sb=$('#sumbtn');if(sb)sb.disabled=!(P.length&&P.length>=S.np)}")
    rep(r"\$\('#stats'\)\.innerHTML=`[^\n]*\n","$('#stats').innerHTML=`<div><b>${km} km</b>distance</div><div><b>${Math.round(km*7.5*DEN[ri]*AMB[PROF.amb].r)} m</b>dénivelé</div><div><b>${Math.min(99,CALM[ri]-AMB[PROF.amb].c)}%</b>routes calmes</div>`;\n",True)
    # init at end: before first render() call at top level
    rep("$('#gpx').onclick=()=>alert('Démo : le GPX sera généré ici.');","$('#gpx').onclick=()=>alert('Démo : le GPX sera généré ici.');$('#sumbtn').onclick=openSum;$('#sumx').onclick=closeSum;document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('#sum').hidden)closeSum()});profInit();")
    open(p,'w',encoding='utf-8').write(s)
print('patched')
