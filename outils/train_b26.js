/* ---------- Ride and train, temps B : horaires de retour (fonction Supabase + PRIM) ---------- */
const SRV={url:()=>(OSMS.get('mr_srv')||'').trim(),key:()=>(OSMS.get('mr_srvkey')||'').trim()};
const tInIdf=p=>p.lat>=48.1&&p.lat<=49.25&&p.lng>=1.45&&p.lng<=3.6;
const tp2=n=>String(n).padStart(2,'0');
const tDt=(d,m)=>d.getFullYear()+'-'+tp2(d.getMonth()+1)+'-'+tp2(d.getDate())+'T'+tp2(Math.floor(m/60)%24)+':'+tp2(m%60);
const TRC=new Map();
const SRV_ERR={hors_idf:'Horaires disponibles seulement en Île-de-France',serveur_non_configure:'Serveur : jeton PRIM manquant',cle_refusee:'Jeton PRIM refusé : à vérifier dans Supabase',quota_prim:'Quota PRIM atteint : réessaie plus tard',trop_de_requetes:'Trop de demandes : réessaie dans une minute',prim_injoignable:'PRIM injoignable pour l’instant'};
function srvTrain(st,home,date,min){const k=st.lat.toFixed(4)+','+st.lng.toFixed(4)+'|'+tDt(date,min);if(TRC.has(k))return TRC.get(k);
 const p=fetchT(SRV.url(),{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+SRV.key(),'apikey':SRV.key()},body:JSON.stringify({from:{lat:st.lat,lng:st.lng},to:{lat:home.lat,lng:home.lng},datetime:tDt(date,min)})},15000)
  .then(async r=>{const j=await r.json().catch(()=>({ok:false,reason:'reponse'}));if(!j.ok)throw new Error(SRV_ERR[j.reason]||('Horaires indisponibles ('+(j.reason||r.status)+')'));return j}).catch(e=>{TRC.delete(k);throw e});
 TRC.set(k,p);return p}
const tdOf=s=>{const m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(s);return new Date(+m[1],+m[2]-1,+m[3],12,0,0)};
let _ttSeq=0;
const hmT=m=>{const h=Math.floor(m/60),mm=m%60;return h?h+' h '+tp2(mm):mm+' min'};
const badge=l=>'<span style="display:inline-block;background:#141414;color:#fff;border-radius:8px;padding:1px 8px;font-weight:700;margin-right:4px">'+xe(l.ligne||l.mode||'Train')+'</span>'+xe([l.reseau,l.mode].filter((x,i,a)=>x&&a.indexOf(x)===i).join(' · '));
const lignesH=t=>(t.lignes&&t.lignes.length?t.lignes.map(badge).join(' › '):'Train')+(t.correspondances?' · '+t.correspondances+' corresp.':' · direct');
const velo=(r,min)=>'<span style="color:'+(r.level==='ko'?'#E5484D':r.level==='ok'?'#2E9E4F':'#141414')+'">'+(r.level==='ko'?'✗ Vélo interdit à cette heure':r.level==='ok'?'✓ Vélo accepté':'ℹ Règles vélo à vérifier')+'</span>';
async function trainTimes(){const e=document.getElementById('osm_train');if(!e)return;let b=e.querySelector('#tr_ret');
 if(!b){b=document.createElement('div');b.id='tr_ret';b.style.cssText='margin-top:8px';e.appendChild(b)}
 if(!SRV.url()||!SRV.key()){b.innerHTML='<div style="color:var(--muted)">Horaires des trains : serveur non configuré (Profil › Compte › Horaires de trains).</div>';return}
 const home=gStart();if(!tInIdf(home)){b.innerHTML='<div style="color:var(--muted)">Horaires disponibles seulement pour un retour en Île-de-France.</div>';return}
 const st0=S.tr.st,sel={name:st0.name,lat:st0.lat,lng:st0.lng},list=S.tr.alts.slice(0,4).map(s=>({name:s.name,lat:s.lat,lng:s.lng}));
 const my=++_ttSeq;b.innerHTML='<div style="color:var(--muted)">Recherche des trains de retour…</div>';
 const t0=dayDate(S.dep.day),c=trainCtx();
 const res=await Promise.all(list.map(async s=>{
  const e0=(c&&s.name===sel.name)?c.e:depMin()+Math.round(((c?c.base:S.km)+hav(S.dest,s)*DF.get())/HOURS_RULES.speed*60)+S.np*HOURS_RULES.pauseMin,tb=e0+15,date=dayDate(S.dep.day+Math.floor(tb/1440)),min=tb%1440;
  try{const j=await srvTrain(s,home,date,min);const T=(j.trajets||[]).map(t=>{const dd=tdOf(t.depart_gare.date);return Object.assign({},t,{rules:trainRules(s,dd,t.depart_gare.min),total:Math.round((tdOf(t.arrivee.date)-t0)/86400000)*1440+t.arrivee.min-depMin()})});
   if(!T.length)return{s,err:'Aucun train trouvé à cette heure',e0};return{s,T,t:T[0],total:T[0].total,e0}}catch(er){return{s,err:er.message,e0}}}));
 if(my!==_ttSeq)return;
 const ok=res.filter(x=>x.t),best=ok.length?ok.reduce((a,x)=>x.total<a.total?x:a):null,cur=res.find(x=>x.s.name===sel.name),oth=res.filter(x=>x!==cur);
 let h='';
 if(cur&&cur.t){const t=cur.t;
  h+='<div style="border:2px solid var(--ink);border-radius:12px;padding:8px 10px;margin-bottom:8px"><div style="font-weight:700">Train conseillé · arrivée à la gare vers '+fh(cur.e0)+'</div>'
   +'<div style="margin:4px 0">'+lignesH(t)+'</div><div><b>'+fh(t.depart_gare.min)+'</b> départ de '+xe(cur.s.name)+' → <b>'+fh(t.arrivee.min)+'</b> chez toi ('+hmT(t.duree_min)+')</div><div>'+velo(t.rules)+'</div></div>'
   +'<div style="font-weight:700;margin:6px 0 2px">Prochains trains (si tu as du retard)</div><ul style="list-style:none;margin:0;padding:0">'
   +cur.T.map((u,i)=>'<li style="padding:5px 0;border-top:1px solid #ddd"><b>'+fh(u.depart_gare.min)+'</b> → '+fh(u.arrivee.min)+' · '+hmT(u.duree_min)+(i===0?' <span style="color:var(--muted)">(prévu)</span>':'')+'<br>'+lignesH(u)+'<br>'+velo(u.rules)+'</li>').join('')+'</ul>'}
 else if(cur){h+='<div style="padding:6px 8px;border:1.5px solid #bbb;border-radius:10px"><b>'+xe(cur.s.name)+'</b><br><span style="color:var(--muted)">'+xe(cur.err)+'</span></div>'}
 if(oth.length){h+='<div style="font-weight:700;margin:10px 0 2px">Autres gares possibles</div>'+oth.map(x=>{const i=res.indexOf(x);
  if(!x.t)return'<div style="margin:4px 0;padding:6px 8px;border:1.5px solid #bbb;border-radius:10px"><b>'+xe(x.s.name)+'</b><br><span style="color:var(--muted)">'+xe(x.err)+'</span></div>';
  return'<button type="button" data-i="'+i+'" style="display:block;width:100%;text-align:left;margin:4px 0;padding:6px 8px;border:2px solid #bbb;border-radius:10px;background:#fff;font:inherit;cursor:pointer"><b>'+xe(x.s.name)+'</b>'+(x===best?' <span style="background:#FFD21F;border-radius:8px;padding:1px 6px;font-weight:700">Le plus rapide</span>':'')+'<br>Train à '+fh(x.t.depart_gare.min)+' · chez toi à '+fh(x.t.arrivee.min)+' · sortie de '+hmT(x.total)+'<br>'+lignesH(x.t)+'</button>'}).join('')}
 else if(best===cur&&cur&&cur.t)h+='';
 if(cur&&cur.t&&best&&best!==cur)h+='<div style="margin-top:4px"><span style="background:#FFD21F;border-radius:8px;padding:1px 6px;font-weight:700">Plus rapide : '+xe(best.s.name)+'</span></div>';
 h+='<div style="color:var(--muted);margin-top:6px">Horaires théoriques et prévisions PRIM, à vérifier avant le départ.</div>';
 b.innerHTML=h;
 b.querySelectorAll('button[data-i]').forEach(btn=>btn.onclick=()=>{const x=res[+btn.dataset.i];const a=S.tr.alts.find(z=>z.name===x.s.name);if(a){S.tr.st=a;osmTrain()}})}
/* carte « Retour en train » : après le choix des pauses. Le tracé va jusqu'au lieu d'arrivée, puis jusqu'à la gare la plus proche. */
function trainCtx(){const R=S.routeG||S.loopG;if(!R||!S.dest||!S.tr||!S.tr.st||R._legSt!==S.tr.st.name)return null;const base=R._base?R._base.km:R.km,legKm=R.leg?R.leg.km:0,km=base+legKm,e=depMin()+Math.round(km/HOURS_RULES.speed*60)+S.np*HOURS_RULES.pauseMin,tb=e+15,date=dayDate(S.dep.day+Math.floor(tb/1440)),min=tb%1440;return{km,base,legKm,e,tb,date,min,rules:trainRules(S.tr.st,date,min)}}
function trainG(){if(!osmOn()||S.mode!=='train'||!S.dest)return null;const c=trainCtx();return c?[S.tr.st.name,Math.round(c.km)+' km',c.rules.short]:[S.dest.label.split(',')[0],Math.round(S.destKm||S.km)+' km','Ta gare de retour est proposée après le choix des pauses']}
async function trainPrep(R){const key=S.dest.lat.toFixed(4)+','+S.dest.lng.toFixed(4);
 if(!S.tr||S.tr.key!==key)S.tr={key,alts:null,st:null};
 if(!S.tr.alts){let L=[];for(const r of [6,15,35,70]){L=await osmStations(S.dest,r);if(L.length)break}
  S.tr.alts=L.map(s=>({s,d:hav(s,S.dest)})).sort((x,y)=>x.d-y.d).slice(0,4).map(x=>Object.assign({dd:x.d},x.s));S.tr.st=S.tr.alts[0]||null}
 if(!S.tr.st)return false;
 if(!R._base)R._base={path:R.path,km:R.km,gain:R.gain||0};
 if(R._legSt===S.tr.st.name)return true;
 const st=S.tr.st;let chg=false;
 if(hav(S.dest,st)<0.15){R.path=R._base.path;R.km=R._base.km;R.gain=R._base.gain;R.leg=null;chg=true}
 else{const lg=await RoutingORS.compute({lat:S.dest.lat,lng:S.dest.lng},{lat:st.lat,lng:st.lng},[]);R.path=R._base.path.concat(lg.path.slice(1));R.km=R._base.km+lg.km;R.gain=R._base.gain+(lg.gain||0);R.leg={km:lg.km,min:lg.durMin};chg=true}
 R._legSt=st.name;if(chg){try{drawMap(true)}catch(e){}try{osmStats()}catch(e){}}return true}
let _trTok=0;
osmTrain=function(){let e=document.getElementById('osm_train');const done=S.picks&&S.picks.filter(Boolean).length>=S.np,R=S.routeG||S.loopG;
 if(!osmOn()||S.mode!=='train'||!S.gen||!done||!S.dest||!R){if(e)e.remove();return}
 if(!e){e=document.createElement('div');e.id='osm_train';e.style.cssText='margin:6px 0 10px;padding:10px 12px;border:2px solid var(--ink);border-radius:16px;font:500 12px/1.45 Poppins,sans-serif;background:#fff';$('#stop').after(e)}
 const my=++_trTok;
 if(!(S.tr&&S.tr.st&&R._legSt===S.tr.st.name&&e.dataset.k===S.tr.st.name+'|'+S.tr.key)){e.innerHTML='<div style="font-weight:700;font-size:13px">Retour en train</div><div style="color:var(--muted)">Recherche de la gare la plus proche…</div>';e.dataset.k=''}
 trainPrep(R).then(ok=>{if(my!==_trTok)return;
  if(!ok){e.innerHTML='<div style="font-weight:700;font-size:13px">Retour en train</div><div>Aucune gare repérée près de '+xe(S.dest.label.split(',')[0])+' : essaie une autre ville.</div>';return}
  const c=trainCtx();if(!c)return;
  const j=['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'][c.date.getDay()],col=c.rules.level==='ko'?'#E5484D':c.rules.level==='ok'?'#2E9E4F':'#141414',st=S.tr.st,place=S.dest.label.split(',')[0],arrP=c.e-Math.round(c.legKm/HOURS_RULES.speed*60);
  e.style.borderColor=col;
  const k=st.name+'|'+S.tr.key;
  if(e.dataset.k!==k){e.dataset.k=k;
   e.innerHTML='<div style="font-weight:700;font-size:13px;margin-bottom:2px">Retour en train · '+xe(st.name)+'</div><div>Tu arrives à <b>'+xe(place)+'</b> vers '+fh(arrP)+'. '+(c.legKm>0?'Puis '+String(Math.round(c.legKm*10)/10).replace('.',',')+' km jusqu’à la gare (≈ '+Math.max(1,Math.round(c.legKm/HOURS_RULES.speed*60))+' min).':'La gare est juste à côté.')+' À la gare vers '+fh(c.e)+' · '+j+' '+c.date.getDate()+'.</div>'
   +'<details style="margin:6px 0"><summary style="cursor:pointer">Règles vélo dans les trains</summary><ul style="margin:6px 0 6px 16px;padding:0">'+c.rules.lines.map(x=>'<li>'+xe(x)+'</li>').join('')+'</ul></details><div id="tr_ret" style="margin-top:8px"></div>'}
  trainTimes()}).catch(er=>{if(my!==_trTok)return;e.innerHTML='<div style="font-weight:700;font-size:13px">Retour en train</div><div>'+xe(er.message||'Gare indisponible')+'</div>'})};
{const s0=showRes;showRes=function(){const r=s0.apply(this,arguments);try{osmTrain()}catch(e){}return r}}
function trainUI(){const o=document.getElementById('tr_sel');if(o)o.remove()}
/* réglages du serveur d'horaires (Profil › Compte) */
(()=>{const P=document.querySelector('.psub[data-t="Compte"]');if(!P)return;const box=document.createElement('div');
 box.innerHTML='<h2 class="st" style="font-size:16px;margin:14px 0 0">Horaires de trains</h2><div class="set"><div class="row"><input id="srv_url" type="url" placeholder="Adresse de la fonction Supabase" style="width:100%"></div><div class="row"><input id="srv_key" type="password" placeholder="Clé « anon » du projet Supabase" style="width:100%"></div><div class="row"><button type="button" id="srv_test" class="lnk">Tester</button><span id="srv_msg" class="sub" style="font-size:12px"></span></div></div><p class="sub" style="font-size:12px;margin:6px 2px 0">Le jeton PRIM n’est jamais ici : il reste dans les secrets de Supabase. La clé « anon » est publique par conception.</p>';P.appendChild(box);
 const u=box.querySelector('#srv_url'),k=box.querySelector('#srv_key'),m=box.querySelector('#srv_msg');u.value=SRV.url();k.value=SRV.key();
 u.onchange=()=>{OSMS.set('mr_srv',u.value.trim());TRC.clear()};k.onchange=()=>{OSMS.set('mr_srvkey',k.value.trim());TRC.clear()};
 box.querySelector('#srv_test').onclick=async()=>{OSMS.set('mr_srv',u.value.trim());OSMS.set('mr_srvkey',k.value.trim());TRC.clear();m.textContent='Test…';try{const d=new Date();d.setDate(d.getDate()+1);const j=await srvTrain({lat:48.8049,lng:2.1264},{lat:48.8443,lng:2.3744},d,10*60);m.textContent=j.trajets.length?'OK : '+j.trajets.length+' trajet(s), arrivée '+fh(j.trajets[0].arrivee.min):'Serveur joint, aucun train trouvé'}catch(e){m.textContent=e.message}}})();
