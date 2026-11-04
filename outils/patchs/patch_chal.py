import re
for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new,cnt=1):
        global s
        assert s.count(old)==cnt,(f,old[:80],s.count(old))
        s=s.replace(old,new)
    # ---------- A. données : remplace CHAL / BADGES / XPOF ----------
    s,k=re.subn(r"const CHAL=\[.*?\];\n","",s,count=1,flags=re.S);assert k==1
    s,k=re.subn(r"const BADGES=\[.*?\];\n","",s,count=1,flags=re.S);assert k==1
    s,k=re.subn(r"const XPOF=\(\)=>[^\n]*\n","",s,count=1);assert k==1
    core=r"""
const pad2=n=>String(n).padStart(2,'0'),YM=d=>d.slice(0,7);
const todayIso=()=>{const d=new Date();return d.getFullYear()+'-'+pad2(d.getMonth()+1)+'-'+pad2(d.getDate())},curYM=()=>todayIso().slice(0,7);
const fH=h=>{h=((h%24)+24)%24;let a=Math.floor(h),m=Math.round((h-a)*60);if(m===60){a=(a+1)%24;m=0}return a+' h '+pad2(m)};
let CLAIM=null;try{CLAIM=JSON.parse(localStorage.getItem('mr_claim')||'null')}catch(e){}
const saveClaim=()=>{try{localStorage.setItem('mr_claim',JSON.stringify(CLAIM))}catch(e){}};
const CHD=[
 ['pause','Pause gourmande ×3','Passer dans 3 boulangeries différentes ce mois-ci',3,100,R=>new Set(R.flatMap(r=>r[5].map(x=>x[0]))).size],
 ['km100','Sortie de 100 km','Rouler 100 km en une seule sortie',100,200,R=>Math.max(0,...R.map(r=>r[2])),'km'],
 ['early','Lève-tôt','Partir avant 8 h (validé dès le départ)',1,100,R=>R.some(r=>r[6]!=null&&r[6]<8)?1:0],
 ['noon','Matinal','Terminer une sortie avant midi',1,100,R=>R.some(r=>r[6]!=null&&r[6]+r[3]<12)?1:0],
 ['reg','Régulier','Faire 5 sorties dans le mois',5,150,R=>R.length],
 ['train','Ride and train','Faire un trajet aller en train',1,120,R=>R.some(r=>r[7]==='train')?1:0]];
const monthRides=ym=>RIDES.filter(r=>YM(r[0])===ym);
const chalNow=ym=>{ym=ym||curYM();const R=monthRides(ym);return CHD.map(d=>[d[1],d[2],Math.min(d[3],d[5](R)),d[3],d[4],d[0],d[6]||'',!!((CLAIM||{})[ym]||{})[d[0]]])};
const claimedXP=()=>Object.values(CLAIM||{}).reduce((a,m)=>a+Object.values(m).reduce((b,x)=>b+x,0),0);
const XPOF=()=>ME.km+claimedXP();
function claimCalc(ym,extra,only){const R=monthRides(ym).concat(extra?[extra]:[]),got=(CLAIM||{})[ym]||{};return CHD.filter(d=>(!only||only.includes(d[0]))&&!got[d[0]]&&d[5](R)>=d[3]).map(d=>({id:d[0],t:d[1],xp:d[4]}))}
function claimApply(ym,L){if(!L.length)return L;CLAIM=CLAIM||{};CLAIM[ym]=CLAIM[ym]||{};L.forEach(c=>CLAIM[ym][c.id]=c.xp);saveClaim();return L}
const startChal=h=>{const ym=curYM();return claimApply(ym,claimCalc(ym,[todayIso(),'',0,0,0,[],h,''],['early']))};
const shopsN=()=>9+[...new Set(RIDES.flatMap(r=>r[5].map(x=>x[0])))].filter(n=>!SEEDSHOPS.has(n)).length;
const BD=[['Première sortie','wheel',()=>ME.rides>=1],['100 km d’une traite','road',()=>RIDES.some(r=>r[2]>=100)],['Lève-tôt','sun',()=>RIDES.some(r=>r[6]!=null&&r[6]<8)],['Gourmand · 10 boulangeries','gift',()=>shopsN()>=10],['Voyageur du rail','train',()=>RIDES.some(r=>r[7]==='train')],['1 000 km','star',()=>ME.km>=1000],['5 000 km','star',()=>ME.km>=5000]];
const badgesNow=()=>BD.map(b=>[b[0],b[1],!!b[2]()]);
const saveRide=r=>{try{const sv=JSON.parse(localStorage.getItem('mr_rides')||'[]');sv.unshift(r);localStorage.setItem('mr_rides',JSON.stringify(sv.slice(0,50)))}catch(e){}};
function previewDone(rr,startSum){startSum=startSum||0;const b0=badgesNow(),km0=ME.km,n0=ME.rides,kx=Math.max(1,Math.round(rr[2]));
 RIDES.unshift(rr);ME.km+=kx;ME.rides++;const claims=claimCalc(YM(rr[0]),null),b1=badgesNow();RIDES.shift();ME.km=km0;ME.rides=n0;
 return{base:XPOF()-startSum,gain:kx+startSum+claims.reduce((a,c)=>a+c.xp,0),claims,badges:b1.filter((b,i)=>b[2]&&!b0[i][2]).map(b=>b[0])}}
function finishRide(rr,startSum){startSum=startSum||0;const base=XPOF()-startSum,b0=badgesNow(),kx=Math.max(1,Math.round(rr[2]));
 RIDES.unshift(rr);ME.km+=kx;ME.rides++;saveRide(rr);const claims=claimApply(YM(rr[0]),claimCalc(YM(rr[0]),null)),b1=badgesNow();
 return{base,gain:kx+startSum+claims.reduce((a,c)=>a+c.xp,0),claims,badges:b1.filter((b,i)=>b[2]&&!b0[i][2]).map(b=>b[0])}}
const bonusHTML=(cl,bd)=>(cl.length||bd.length)?`<div class="bon">${cl.map(c=>`<div class="bl"><i>✓</i><span>Défi validé : <b>${c.t}</b></span><em>+${c.xp} XP</em></div>`).join('')}${bd.map(b=>`<div class="bl"><i>★</i><span>Badge débloqué : <b>${b}</b></span></div>`).join('')}</div>`:'';
"""
    # insère juste après la ligne ME
    rep("const ME={km:1240,rides:23,shops:9};\n","const ME={km:1240,rides:23,shops:9};\n"+core)
    # ---------- B. RIDES : ajout heure de départ + mode ----------
    for d,h,m in [("2026-10-18",9.6,""),("2026-10-11",9.0,""),("2026-10-04",9.2,"train"),("2026-09-27",7.5,""),("2026-09-20",9.5,""),("2026-09-13",8.0,""),("2026-09-06",9.0,""),("2026-08-30",7.0,"")]:
        pat=re.compile(r'(\["'+d+r'","[^"]*",[\d.]+,[\d.]+,\d+,\[(?:\["[^"]*",\d+\],?)+\])\]')
        s,k=pat.subn(lambda mo:mo.group(1)+f",{h},'{m}']",s,count=1);assert k==1,(f,d)
    # SEEDSHOPS + seed claims, après chargement des sorties enregistrées
    rep("const bakOf=","const SEEDSHOPS=new Set(RIDES.flatMap(r=>r[5].map(x=>x[0])));\nconst bakOf=")
    m=re.search(r"try\{const sv=JSON\.parse\(localStorage\.getItem\('mr_rides'\)\|\|'\[\]'\);if\(Array\.isArray\(sv\)\)sv\.forEach\(r=>\{RIDES\.unshift\(r\);ME\.km\+=Math\.round\(r\[2\]\);ME\.rides\+\+\}\)\}catch\(e\)\{\}",s);assert m,f
    s=s[:m.end()]+"\nif(!CLAIM){CLAIM={};const ym=curYM(),R=monthRides(ym);CLAIM[ym]={};CHD.forEach(d=>{if(d[5](R)>=d[3])CLAIM[ym][d[0]]=d[4]});saveClaim()}"+s[m.end():]
    # ---------- C. Fidélité : défis / badges dynamiques ----------
    rep("const ch=CHAL.map(c=>{const d=c[2]>=c[3];return `<div class=\"ch${d?' ok':''}\"><div class=\"r\"><b>${c[0]}${d?' ✓':''}</b><span class=\"xp\">+${c[4]} XP</span></div><small>${c[1]}</small>",
        "const ch=chalNow().map(c=>{const d=c[2]>=c[3],pg=c[6]==='km'?Math.round(c[2])+' / '+c[3]+' km':c[2]+' / '+c[3];return `<div class=\"ch${d?' ok':''}\"><div class=\"r\"><b>${c[0]}${d?' ✓':''}</b><span class=\"xp\">+${c[4]} XP</span></div><small>${c[1]} · ${pg}</small>")
    rep("const bg=BADGES.map(","const bg=badgesNow().map(")
    rep("<b>${CHAL.filter(c=>c[3]<=c[2]).length} défis</b>","<b>${chalNow().filter(c=>c[2]>=c[3]).length} défis</b>")
    rep("<h2 style=\"font-size:16px;margin:18px 0 0\">Défis en cours</h2>${ch}","<h2 style=\"font-size:16px;margin:18px 0 0\">Défis de ${new Date().toLocaleDateString('fr-FR',{month:'long'})}</h2><p class=\"sub\" style=\"font-size:12px;margin:2px 0 0\">Ils repartent à zéro le 1er du mois.</p>${ch}")
    rep("$('#mS').textContent=ME.shops}","$('#mS').textContent=shopsN()}")
    # historique : heure de départ
    rep("${String(r[2]).replace('.',',')} km · ${fmtH(r[3])} · ${r[4]} m</span>","${String(r[2]).replace('.',',')} km · ${fmtH(r[3])} · ${r[4]} m${r[6]!=null?' · départ '+fH(r[6]):''}</span>")
    # ---------- D. css ----------
    css=r""".bon{display:flex;flex-direction:column;gap:6px;margin-top:10px;width:100%}
.bon .bl{display:flex;align-items:center;gap:8px;border:2px solid var(--ink);border-radius:14px;background:var(--yellow);padding:7px 10px;font:600 13px Poppins,sans-serif;color:#141414;text-align:left;animation:xpop .5s both}
.bon .bl i{flex:none;width:22px;height:22px;border-radius:50%;background:#141414;color:var(--yellow);display:flex;align-items:center;justify-content:center;font-style:normal;font-size:12px;font-weight:800}
.bon .bl span{flex:1}.bon .bl em{font:800 13px Poppins,sans-serif;font-style:normal;white-space:nowrap}
"""
    rep(".lo{display:block;",css+".lo{display:block;")
    # ---------- E. celebrate : défis + badges ----------
    rep("<div class=\"cst\"><div><b>${String(o.km).replace('.',',')} km</b>distance</div><div><b>${o.dur}</b>durée</div><div><b>${o.pct} %</b>du tracé suivi</div></div><button class=\"cgo\"",
        "<div class=\"cst\"><div><b>${String(o.km).replace('.',',')} km</b>distance</div><div><b>${o.dur}</b>durée</div><div><b>${o.pct} %</b>du tracé suivi</div></div>${bonusHTML(o.claims||[],o.badges||[])}<button class=\"cgo\"")
    rep("confetti();xpAnim(o.gain,'ce',o.base);CET.push(setTimeout(()=>$('#cgo').classList.add('on'),T+300));",
        "const nb=(o.claims||[]).length+(o.badges||[]).length;B.querySelectorAll('.bon .bl').forEach((e,i)=>e.style.animationDelay=((T+250)/1000+i*.55)+'s');\n confetti();xpAnim(o.gain,'ce',o.base);CET.push(setTimeout(()=>$('#cgo').classList.add('on'),T+300+nb*550));")
    # ---------- F. sync : utilise finishRide ----------
    a=s.index("  at(5900,()=>{add('Sortie validée'")
    b=s.index(" }else{\n  at(5000,()=>{add('À vérifier'")
    new=r"""  at(5900,()=>{add('Sortie validée','L’XP est ajoutée à ton garage.');q.st='done';savePlans();
   const R=syncRide(q);$('#syx2').innerHTML=`<div class="sybtn"><button type="button" id="syrw">Revoir la récompense</button><button class="y" type="button" id="syok">Voir mon historique</button></div>`;
   const show=(go)=>celebrate({name:q.name,km:R.km,dur:R.dur,pct,gain:R.gain,base:R.base,claims:R.claims,badges:R.badges,done:go?()=>{$('#sy').hidden=true;histRender()}:null});$('#syrw').onclick=()=>show(false);at(900,()=>show(true));
   $('#syok').onclick=()=>{$('#sy').hidden=true;histRender()};histRender()})
"""
    s=s[:a]+new+s[b:]
    # étape détectée : horaires
    rep("at(1500,()=>{add(`Sortie détectée : ${String(km).replace('.',',')} km · ${dur}`,q.name);q.st='sent'});",
        "const sH=q.startH!=null?q.startH:7.7,eH=sH+km/(PROF.speed||25);\n at(1500,()=>{add(`Sortie détectée : ${String(km).replace('.',',')} km · ${dur}`,`${q.name} · départ ${fH(sH)} · arrivée ${fH(eH)}`);q.st='sent'});")
    # helper syncRide + autoValidate
    helper=r"""
function syncRide(q){const sp=PROF.speed||25,km=Math.max(1,Math.round(q.km*1.02*10)/10),hrs=km/sp,startH=q.startH!=null?q.startH:7.7,
 rr=[todayIso(),q.name,km,hrs,Math.round(km*7),(q.stops||[]).map(x=>[x[0],x[1]]),startH,q.mode==='train'?'train':''];
 return Object.assign({km,dur:fmtH(hrs)},finishRide(rr,0))}
"""
    rep("function openSync(i,mode,imp){",helper+"function openSync(i,mode,imp){")
    # autoValidate
    a=s.index("function autoValidate(i){");b=s.index("function maybeAuto(){")
    s=s[:a]+r"""function autoValidate(i){const q=PLANS[i];if(!q||q.st==='done')return;q.st='done';savePlans();const R=syncRide(q);
 celebrate({name:q.name,km:R.km,dur:R.dur,pct:94,gain:R.gain,base:R.base,claims:R.claims,badges:R.badges,done:()=>{showPg('j');histRender()}})}
"""+s[b:]
    rep("PLANS.unshift({id:Date.now(),sess:SESSION,name:S.sumt||'Boucle',km:c.km,via,","PLANS.unshift({id:Date.now(),sess:SESSION,mode:S.mode,name:S.sumt||'Boucle',km:c.km,via,")
    open(p,'w',encoding='utf-8').write(s);print(f,'part1 ok')
