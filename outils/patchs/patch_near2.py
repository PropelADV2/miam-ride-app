for f in ['accueil-velo.html','miam-ride-osm.html','introduction-miam-ride.html']:
    p='/mnt/user-data/outputs/'+f;s=open(p,encoding='utf-8').read()
    def rep(a,b):
        global s
        assert s.count(a)==1,(f,a[:80],s.count(a));s=s.replace(a,b)
    rep("`<button type=\"button\" data-pp=\"${i}:${k}\">Je suis chez ${x[0]}</button>`}).join('')}</div>`:''}","`<button type=\"button\" data-pp=\"${i}:${k}\">Je suis chez ${x[0]}</button>`}).join('')}${q.st!=='done'&&q.stops.some(x=>!(q.pass||[]).includes(x[0]))?`<button type=\"button\" class=\"dmo2\" data-nr=\"${i}\">Démo : j’approche de la prochaine boulangerie (500 m)</button>`:''}</div>`:''}")
    rep(".pps small{",".pps .dmo2{border:0;background:transparent;color:var(--muted);font:600 11.5px Poppins,sans-serif;text-decoration:underline;padding:0}.pps small{")
    rep("H.querySelectorAll('[data-pp]').forEach(","H.querySelectorAll('[data-nr]').forEach(b=>b.onclick=()=>{const i=+b.dataset.nr,q=PLANS[i];if(!q||!q.stops)return;const k=q.stops.findIndex(x=>!(q.pass||[]).includes(x[0]));if(k<0)return;if(!nearOn()){pushNote('Alerte désactivée','Active-la dans ton profil pour être prévenu à 500 m.')}else pushNote(`${q.stops[k][0]} dans 500 m`,'Prépare ton QR code. '+nearTxt,'Ouvrir mon QR code',()=>planPass(i,k))});\n H.querySelectorAll('[data-pp]').forEach(")
    rep("profInit();(()=>{const e=$('#f_dh');","profInit();(()=>{const n=$('#f_near');if(n){n.value=nearOn()?'1':'0';n.onchange=()=>{try{localStorage.setItem('mr_near',n.value)}catch(x){}}}})();(()=>{const e=$('#f_dh');")
    open(p,'w',encoding='utf-8').write(s)
