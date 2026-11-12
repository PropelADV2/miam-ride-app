# vers 31 : « Vers un lieu » = meilleur tracé uniquement + « autre trajet » ; « Boucle » = « une autre boucle »
s=open('/mnt/user-data/outputs/Miam ride osm - vers 30.html').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:70],s.count(a)); s=s.replace(a,b)
# 1. Vers un lieu : toujours le meilleur tracé, plus de bascule Boucle
rep("tdist:false,fast:false,","tdist:false,fast:true,")
i=s.index("  const sw=m==='dest'?`<div class=\"opts\"");j=s.index("\n",i)
s=s[:i]+"  const sw='';"+s[j:]
rep("(fast?'La boucle la plus rapide':'Une boucle via mon arrivée')","'Le meilleur tracé jusqu’à ton arrivée'")
rep("(fast?'On passe par ton arrivée, à mi-parcours, et on revient par un autre chemin. Pas de distance à choisir.':'Choisis la distance : on passe par ton arrivée, à mi-parcours, et on boucle.')","'Choisis ton lieu d’arrivée dans la barre du haut : on trace le meilleur chemin, avec tes pauses boulangerie sur la route. Un autre trajet reste possible ensuite.'")
rep("  p.querySelectorAll('[data-f]').forEach(b=>b.onclick=()=>{S.fast=b.dataset.f==='1';render()});\n","")
rep("Vers un lieu<small>Boucle via l’arrivée</small>","Vers un lieu<small>Le meilleur tracé</small>")
rep("'Lieu d’arrivée, à mi-parcours'","'Lieu d’arrivée'")
rep('placeholder="Lieu d’arrivée, à mi-parcours"','placeholder="Lieu d’arrivée"')
rep("S.sumt=(S.mode==='dest'&&S.fast)?'Le plus rapide':MN[S.mode]","S.sumt=MN[S.mode]")
# 2. variantes de tracé
rep("const gBearing=()=>((S.sel||0)*40)%360;","const gBearing=()=>((S.sel||0)*40+(S.vary||0)*47)%360;")
rep("  const r=await RoutingORS.compute(c,D,[],true);OSMT.orsN++;r.dest=D;r.waypoints=[];","  const r=(S.mode==='dest'&&S.vary)?await altDest(c,D,d):await RoutingORS.compute(c,D,[],true);OSMT.orsN++;r.dest=D;r.waypoints=r.mids||(r.via?[r.via]:[]);")
rep(" if(out.length){out.sort((x,y)=>ambScore(x,km)-ambScore(y,km));best=out[0];"," if(out.length){fresh(out);out.sort((x,y)=>ambScore(x,km)-ambScore(y,km));best=out[0];")
rep(" if(out.length){out.sort((x,y)=>ambScore(x,target)-ambScore(y,target));let best=out[0];"," if(out.length){fresh(out);out.sort((x,y)=>ambScore(x,target)-ambScore(y,target));let best=out[0];")
# 3. bouton + réinitialisation
rep('<div class="stats" id="stats"></div>','<div class="stats" id="stats"></div>\n      <button class="mre" id="regen" type="button" hidden></button>')
JS=r"""<script id="v31">
/* ===== vers 31 : autre trajet / autre boucle ===== */
function pathOverlap(A,B){if(!A||!B||A.length<2||B.length<2)return 0;const g=new Set();
 B.forEach(p=>{const a=Math.round(p.lat*400),b=Math.round(p.lng*270);for(let i=-1;i<=1;i++)for(let j=-1;j<=1;j++)g.add((a+i)+','+(b+j))});
 let n=0,t=0;const st=Math.max(1,Math.floor(A.length/60));for(let i=0;i<A.length;i+=st){t++;if(g.has(Math.round(A[i].lat*400)+','+Math.round(A[i].lng*270)))n++}return t?n/t:0}
/* écarte les tracés déjà proposés, s'il en reste de différents */
function fresh(out){if(!S.vary||!S.seen||!S.seen.length)return;const f=out.filter(r=>r.path&&S.seen.every(p=>pathOverlap(r.path,p)<0.7));if(f.length)out.splice(0,out.length,...f);else S.noNew=true}
/* autre trajet vers le même lieu : même critères (ambiance, détour limité), chemin différent */
async function altDest(c,D,d){
 const dx=(D.lng-c.lng)*111.32*Math.cos(c.lat*RAD),dy=(D.lat-c.lat)*110.57,len=Math.hypot(dx,dy)||1,px=-dy/len,py=dx/len;
 const W=(a,l)=>offKm(c,dx*a+px*l*d,dy*a+py*l*d);
 const sets=[[[.5,.13],[.5,-.13],[.35,.2],[.65,-.2]],[[.5,.24],[.5,-.24],[.3,-.14],[.7,.14]]],pick=sets[((S.vary||1)-1)%2];
 const base=S.seen&&S.seen[0]?null:null,out=[];
 OSMP('Recherche d’un autre trajet…');
 await Promise.race([Promise.allSettled(pick.map(async([a,l])=>{const w=W(a,l);OSMT.orsN++;const r=await RoutingORS.compute(c,D,[w],true);r.via=w;r.mids=r.mids||[w];out.push(r)})),new Promise(r=>setTimeout(r,25000))]);
 if(!out.length)throw usrErr('Aucun autre trajet trouvé pour le moment : réessaie dans un instant');
 const amb=AMBT[PROF.amb]||AMBT[1],ref=Math.min(...out.map(x=>x.km),S.destKm||1e9);
 /* critères : détour limité, et ambiance respectée si au moins un tracé la respecte */
 let ok=out.filter(x=>x.km<=ref*1.3+2);if(!ok.length)ok=out.slice();
 const calmOk=ok.filter(x=>(x.calm||0)>=amb.calm-6);if(calmOk.length)ok=calmOk;
 const nw=ok.filter(r=>S.seen.every(p=>pathOverlap(r.path,p)<0.8));if(nw.length)ok=nw;else S.noNew=true;
 ok.sort((x,y)=>ambScore(x,ref)-ambScore(y,ref));const r=ok[0];
 r.amb={i:PROF.amb,target:amb.calm,n:out.length,calms:out.map(x=>x.calm),met:(r.calm||0)>=amb.calm};return r}
/* mémorise chaque tracé proposé */
{const g=gPrepare;gPrepare=async function(){const r=await g.apply(this,arguments);try{S.seen=S.seen||[];if(S.loopG&&S.loopG.path)S.seen.push(S.loopG.path)}catch(e){}return r}}
{const g=gBusy;gBusy=function(on){g.apply(this,arguments);const r=document.getElementById('regen');if(r)r.disabled=!!on}}
function regenUI(){const b=document.getElementById('regen');if(!b)return;const on=!!(S.gen&&(S.mode==='boucle'||S.mode==='dest')&&S.loopG);b.hidden=!on;
 b.textContent=S.mode==='dest'?'Proposer un autre trajet':'Générer une autre boucle'}
{const sr=showRes;showRes=function(){const r=sr.apply(this,arguments);try{regenUI()}catch(e){}return r}}
document.getElementById('go').addEventListener('click',()=>{if(!S.gen){if(!S.regen){S.vary=0;S.seen=[]}S.regen=false;S.noNew=false}},true);
document.getElementById('regen').onclick=()=>{if(!S.gen||!S.loopG)return;S.regen=true;S.vary=(S.vary||0)+1;S.gen=false;S.picks=[];S.active=0;S.loopG=null;S.routeG=null;S.osmEarly=null;OSMC.key=null;OSMC.k2=null;S.gKey=null;
 document.getElementById('go').click();
 const iv=setInterval(()=>{if(S.loopG||!document.getElementById('go').disabled){clearInterval(iv);setTimeout(()=>{if(S.noNew&&typeof osmToast==='function')osmToast('Pas de tracé vraiment différent trouvé : voici le plus proche')},300)}},500);setTimeout(()=>clearInterval(iv),60000)};
</script>
"""
i=s.rindex("</body>");s=s[:i]+JS+s[i:]
open('/mnt/user-data/outputs/Miam ride osm - vers 31.html','w').write(s);print(len(s))
