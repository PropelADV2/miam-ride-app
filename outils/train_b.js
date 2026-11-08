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
async function trainTimes(){const e=document.getElementById('osm_train');if(!e)return;let b=e.querySelector('#tr_ret');
 if(!b){b=document.createElement('div');b.id='tr_ret';b.style.cssText='margin-top:8px;padding-top:8px;border-top:1px dashed #999';e.appendChild(b)}
 if(!SRV.url()||!SRV.key()){b.innerHTML='<div style="color:var(--muted)">Horaires des trains : serveur non configuré (Profil › Compte › Horaires de trains).</div>';return}
 const home=gStart();if(!tInIdf(home)){b.innerHTML='<div style="color:var(--muted)">Horaires disponibles seulement pour un retour en Île-de-France.</div>';return}
 const sel=S.dest,list=(S.trainAlt&&S.trainAlt.length?S.trainAlt:[{name:sel.label,lat:sel.lat,lng:sel.lng}]).slice(0,4).map(s=>({name:s.name,lat:s.lat,lng:s.lng}));
 if(!list.some(s=>s.name===sel.label))list.unshift({name:sel.label,lat:sel.lat,lng:sel.lng});
 const my=++_ttSeq;b.innerHTML='<div style="color:var(--muted)">Recherche des trains de retour…</div>';
 const t0=dayDate(S.dep.day),c=trainCtx();
 const res=await Promise.all(list.map(async s=>{
  const e0=(c&&s.name===sel.label)?c.e:depMin()+Math.round(hav(gStart(),s)*DF.get()/HOURS_RULES.speed*60)+S.np*HOURS_RULES.pauseMin,tb=e0+15,date=dayDate(S.dep.day+Math.floor(tb/1440)),min=tb%1440;
  try{const j=await srvTrain(s,home,date,min);const t=j.trajets&&j.trajets[0];if(!t)return{s,err:'Aucun train trouvé à cette heure',e0};
   const dd=tdOf(t.depart_gare.date),rules=trainRules(s,dd,t.depart_gare.min),fin=Math.round((tdOf(t.arrivee.date)-t0)/86400000)*1440+t.arrivee.min-depMin();
   return{s,t,rules,total:fin,e0}}catch(er){return{s,err:er.message,e0}}}));
 if(my!==_ttSeq)return;
 const ok=res.filter(x=>x.t),best=ok.length?ok.reduce((a,x)=>x.total<a.total?x:a):null;
 const hm=m=>{const h=Math.floor(m/60),mm=m%60;return h?h+' h '+tp2(mm):mm+' min'};
 b.innerHTML='<div style="font-weight:700;font-size:13px;margin-bottom:4px">Rentrer chez toi, gare par gare</div>'+res.map((x,i)=>{
  const cur=x.s.name===sel.label;
  if(!x.t)return'<div style="margin:4px 0;padding:6px 8px;border:1.5px solid #bbb;border-radius:10px"><b>'+xe(x.s.name)+'</b><br><span style="color:var(--muted)">'+xe(x.err)+'</span></div>';
  const lg=x.t.lignes.map(l=>(l.mode+' '+l.ligne).trim()).filter(Boolean).join(' › '),col=x.rules.level==='ko'?'#E5484D':x.rules.level==='ok'?'#2E9E4F':'#141414';
  return'<button type="button" data-i="'+i+'" style="display:block;width:100%;text-align:left;margin:4px 0;padding:6px 8px;border:2px solid '+(cur?'var(--ink)':'#bbb')+';border-radius:10px;background:#fff;font:inherit;cursor:pointer"><b>'+xe(x.s.name)+'</b>'+(x===best?' <span style="background:#FFD21F;border-radius:8px;padding:1px 6px;font-weight:700">Le plus rapide</span>':'')+(cur?' <span style="color:var(--muted)">· gare choisie</span>':'')
   +'<br>Train à '+fh(x.t.depart_gare.min)+' · chez toi à '+fh(x.t.arrivee.min)+' · trajet '+hm(x.t.duree_min)+(x.t.correspondances?' · '+x.t.correspondances+' corresp.':' · direct')+'<br><span style="color:var(--muted)">'+xe(lg)+' · durée totale de la sortie '+hm(x.total)+'</span><br><span style="color:'+col+'">Vélo : '+xe(x.rules.short)+'</span></button>'}).join('')
  +'<div style="color:var(--muted);margin-top:4px">Horaires théoriques et prévisions PRIM, à vérifier avant le départ.</div>';
 b.querySelectorAll('button[data-i]').forEach(btn=>btn.onclick=()=>{const x=res[+btn.dataset.i];if(x.s.name===sel.label)return;const a=(S.trainAlt||[]).find(z=>z.name===x.s.name)||x.s;setTrainDest(a);drawAlt();osmToast('Gare changée : relance le tracé pour l’arriver à '+x.s.name)})}
{const o2=osmTrain;osmTrain=function(){o2.apply(this,arguments);try{if(document.getElementById('osm_train'))trainTimes()}catch(e){}}}
/* réglages du serveur d'horaires (Profil › Compte) */
(()=>{const P=document.querySelector('.psub[data-t="Compte"]');if(!P)return;const box=document.createElement('div');
 box.innerHTML='<h2 class="st" style="font-size:16px;margin:14px 0 0">Horaires de trains</h2><div class="set"><div class="row"><input id="srv_url" type="url" placeholder="Adresse de la fonction Supabase" style="width:100%"></div><div class="row"><input id="srv_key" type="password" placeholder="Clé « anon » du projet Supabase" style="width:100%"></div><div class="row"><button type="button" id="srv_test" class="lnk">Tester</button><span id="srv_msg" class="sub" style="font-size:12px"></span></div></div><p class="sub" style="font-size:12px;margin:6px 2px 0">Le jeton PRIM n’est jamais ici : il reste dans les secrets de Supabase. La clé « anon » est publique par conception.</p>';P.appendChild(box);
 const u=box.querySelector('#srv_url'),k=box.querySelector('#srv_key'),m=box.querySelector('#srv_msg');u.value=SRV.url();k.value=SRV.key();
 u.onchange=()=>{OSMS.set('mr_srv',u.value.trim());TRC.clear()};k.onchange=()=>{OSMS.set('mr_srvkey',k.value.trim());TRC.clear()};
 box.querySelector('#srv_test').onclick=async()=>{OSMS.set('mr_srv',u.value.trim());OSMS.set('mr_srvkey',k.value.trim());TRC.clear();m.textContent='Test…';try{const d=new Date();d.setDate(d.getDate()+1);const j=await srvTrain({lat:48.8049,lng:2.1264},{lat:48.8443,lng:2.3744},d,10*60);m.textContent=j.trajets.length?'OK : '+j.trajets.length+' trajet(s), arrivée '+fh(j.trajets[0].arrivee.min):'Serveur joint, aucun train trouvé'}catch(e){m.textContent=e.message}}})();
