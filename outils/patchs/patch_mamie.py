for f in ['accueil-velo.html','miam-ride-osm.html','introduction-miam-ride.html']:
    p='/mnt/user-data/outputs/'+f;s=open(p,encoding='utf-8').read()
    def rep(a,b,n=1):
        global s
        assert s.count(a)==n,(f,a[:80],s.count(a));s=s.replace(a,b)
    old="<p class=\"sub\" id=\"mq2\" style=\"margin:4px 0 0;font-weight:600;color:var(--ink)\"></p>`;"
    rep(old,"<p class=\"sub\" id=\"mq2\" style=\"margin:4px 0 0;font-weight:600;color:var(--ink)\"></p><button class=\"mre\" id=\"mre\" type=\"button\" hidden>Une autre surprise</button>`;")
    rep("else{g.hidden=false;$('#cs').hidden=true}}","else{const ok=!!(S.gen&&full);g.hidden=ok;$('#cs').hidden=!ok;g.textContent='Mamie, à toi de jouer';const r=$('#mre');if(r){r.hidden=!ok;r.onclick=()=>$('#go').onclick()}}}")
    rep(".pps{margin-top:10px;",".mre{margin-top:8px;border:2px solid var(--ink);border-radius:99px;background:#fff;color:var(--ink);padding:6px 12px;font:700 12.5px Poppins,sans-serif;cursor:pointer}.pps{margin-top:10px;")
    open(p,'w',encoding='utf-8').write(s)
