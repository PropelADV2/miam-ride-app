for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new):
        global s
        assert s.count(old)==1,(f,old[:70],s.count(old))
        s=s.replace(old,new)
    rep("const savePlans=()=>","const SESSION=String(Date.now());let AUTOD=false;\nconst savePlans=()=>")
    rep("PLANS.unshift({id:Date.now(),name:S.sumt||'Boucle',km:c.km,via,st:'sent',","PLANS.unshift({id:Date.now(),sess:SESSION,name:S.sumt||'Boucle',km:c.km,via,st:'sent',")
    js=r"""
function autoValidate(i){const q=PLANS[i];if(!q||q.st==='done')return;const km=Math.max(1,Math.round(q.km*1.02*10)/10),dur=fmtH(km/(PROF.speed||25)),gain=Math.max(1,Math.round(km)),base=XPOF();
 q.st='done';savePlans();
 const d=new Date(),iso=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'),rr=[iso,q.name,km,km/(PROF.speed||25),Math.round(km*7),(q.stops||[]).map(x=>[x[0],x[1]])];
 RIDES.unshift(rr);ME.km+=Math.round(km);ME.rides++;try{const sv=JSON.parse(localStorage.getItem('mr_rides')||'[]');sv.unshift(rr);localStorage.setItem('mr_rides',JSON.stringify(sv.slice(0,50)))}catch(e){}
 celebrate({name:q.name,km,dur,pct:94,gain,base,done:()=>{showPg('j');histRender()}})}
function maybeAuto(){if(AUTOD)return;const I=$('#intro'),A=$('#auth');if((I&&!I.hidden)||(A&&!A.hidden))return;
 const i=PLANS.findIndex(q=>q.st==='sent'&&q.sess!==SESSION);if(i<0)return;AUTOD=true;setTimeout(()=>autoValidate(i),800)}
"""
    rep("function openSync(i,mode,imp){",js+"function openSync(i,mode,imp){")
    # call sites
    rep("const close=()=>{I.hidden=true;try{localStorage.setItem('mr_intro','1')}catch(e){}authGate()};","const close=()=>{I.hidden=true;try{localStorage.setItem('mr_intro','1')}catch(e){}authGate();maybeAuto()};")
    rep("$('#auth').hidden=true;const tb=document.querySelector('.tabbar');if(tb)tb.style.display='';acctUI()}","$('#auth').hidden=true;const tb=document.querySelector('.tabbar');if(tb)tb.style.display='';acctUI();maybeAuto()}")
    rep(" if(!seen)open();else authGate()}"," if(!seen)open();else{authGate();maybeAuto()}}")
    rep("Ta montre envoie la sortie à la fin du parcours : Miam Ride la compare au tracé et la valide.","Ta montre envoie la sortie à la fin du parcours : Miam Ride la compare au tracé et la valide. Démo : un tracé envoyé est validé tout seul à la prochaine ouverture de l’appli.")
    open(p,'w',encoding='utf-8').write(s);print(f,'ok')
