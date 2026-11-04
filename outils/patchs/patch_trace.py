import re
for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new):
        global s
        assert s.count(old)==1,(f,old[:60],s.count(old))
        s=s.replace(old,new)
    # state init in render
    rep("S.mdone=false;S.gen=false;$('#go').textContent","S.mdone=false;S.gen=false;S.traced=false;$('#go').textContent")
    # sumbtn + traced logic
    rep("{const sb=$('#sumbtn');if(sb)sb.disabled=!(P.length&&P.length>=S.np)}",
        "{const full=P.length&&P.length>=S.np,tk=P.map(b=>ALL.indexOf(b)).join()+'/'+S.np;if(m==='mamie')S.traced=!!full;else if(S.traced&&S.tkey!==tk)S.traced=false;S.full=!!full;S.tk=tk;const sb=$('#sumbtn');if(sb)sb.disabled=!(full&&S.traced);const g=$('#go');if(m!=='mamie'){g.textContent=!full?'Je choisis où je me régale':S.traced?'Trajet généré ✓':'Générer le trajet';g.disabled=!!(full&&S.traced)}}")
    # go handler
    rep("$('#go').onclick=()=>{setMin(false);S.gen=true;",
        "$('#go').onclick=()=>{if(S.gen&&S.mode!=='mamie'&&S.full&&!S.traced){S.traced=true;S.tkey=S.tk;setMin(false);showRes();return}\n setMin(false);S.gen=true;S.traced=false;")
    if f=='accueil-velo.html':
        rep("const P=S.gen?Array.from({length:S.np},(_,x)=>S.picks[x]):[],has=P.some(Boolean);\n ['#route','#routeBg'].forEach(q=>{$(q).setAttribute('d',has?r.d:'');",
            "const P=S.gen?Array.from({length:S.np},(_,x)=>S.picks[x]):[],has=P.some(Boolean);\n ['#route','#routeBg'].forEach(q=>{$(q).setAttribute('d',has?r.d:'');$(q).style.visibility=S.traced?'visible':'hidden';")
    else:
        rep("map.getSource('route').setData(has?{type","map.getSource('route').setData(has&&S.traced?{type")
    # reset button state on new generation: handled by showRes
    open(p,'w',encoding='utf-8').write(s);print(f,'ok')
