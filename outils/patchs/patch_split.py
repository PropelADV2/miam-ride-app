for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new):
        global s
        assert s.count(old)==1,(f,old[:60],s.count(old))
        s=s.replace(old,new)
    rep(".ctawrap .cta{margin:0}",".ctawrap .cta{margin:0}\n.ctasplit{display:flex;gap:8px}.ctasplit[hidden]{display:none}\n.ctasplit button{flex:1;margin:0;border:2px solid var(--ink);border-radius:99px;padding:12px 10px;font:800 13px/1.2 Poppins,sans-serif;cursor:pointer;box-shadow:3px 3px 0 var(--ink);color:var(--ink)}\n.ctasplit .cta2{background:#fff}.ctasplit .cta3{background:var(--yellow);text-transform:uppercase}\n.ctasplit button:active{transform:translate(2px,2px);box-shadow:1px 1px 0 var(--ink)}")
    rep('<button class="cta" id="go" type="button">Je choisis où je me régale</button></div>',
        '<button class="cta" id="go" type="button">Je choisis où je me régale</button><div class="ctasplit" id="cs" hidden><button class="cta2" id="cShare" type="button">Partage sur ta montre ou GPS</button><button class="cta3" id="cRun" type="button">Lancer le trajet</button></div></div>')
    rep("g.disabled=!!(full&&S.traced)}}","g.hidden=!!(full&&S.traced);$('#cs').hidden=!g.hidden}else{g.hidden=false;$('#cs').hidden=true}}")
    rep("S.traced=false;$('#go').disabled=false;","S.traced=false;$('#go').disabled=false;$('#go').hidden=false;$('#cs').hidden=true;")
    rep("$('#sumbtn').onclick=openSum;",
        "$('#sumbtn').onclick=openSum;$('#cShare').onclick=()=>{openSum();const t=$('#sumb').querySelector('[data-s]');if(t)t.scrollIntoView({block:'center'})};$('#cRun').onclick=()=>{showPg('r');if(REC.view!=='run')recStart('tracé')};")
    open(p,'w',encoding='utf-8').write(s);print(f,'ok')
