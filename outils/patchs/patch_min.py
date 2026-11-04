for f in ['accueil-velo.html','miam-ride-osm.html','introduction-miam-ride.html']:
    p='/mnt/user-data/outputs/'+f;s=open(p,encoding='utf-8').read()
    def rep(a,b):
        global s
        assert s.count(a)==1,(f,a[:80],s.count(a));s=s.replace(a,b)
    rep("const g=$('#go');if(m!=='mamie'){g.textContent=","if(m!=='mamie'){if(full&&!S.wasFull)setMin(true);S.wasFull=!!full}else S.wasFull=false;const g=$('#go');if(m!=='mamie'){g.textContent=")
    rep("$('#peek').textContent=P.length?`${km} km · ${P.length}/${S.np} pause${S.np>1?'s':''} choisie${P.length>1?'s':''}`:","$('#peek').textContent=P.length?(P.length>=S.np?`${km} km · ${P.length===1?P[0][0]:P.length+' pauses choisies'} · touche la barre pour modifier`:`${km} km · ${P.length}/${S.np} pause${S.np>1?'s':''} choisie${P.length>1?'s':''}`):")
    rep("S.mdone=false;S.gen=false;S.traced=false;$('#go').disabled=false;","S.mdone=false;S.gen=false;S.traced=false;S.wasFull=false;$('#go').disabled=false;")
    rep(" setMin(false);S.gen=true;S.traced=false;S.picks=[];"," setMin(false);S.wasFull=false;S.gen=true;S.traced=false;S.picks=[];")
    open(p,'w',encoding='utf-8').write(s)
