import re
for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    def rep(old,new):
        global s
        assert s.count(old)==1,(f,old[:80],s.count(old))
        s=s.replace(old,new)
    rep("const monthRides=ym=>RIDES.filter(r=>YM(r[0])===ym);","const okR=()=>RIDES.filter(r=>r[8]!==false),monthRides=ym=>okR().filter(r=>YM(r[0])===ym);")
    for a in ["()=>RIDES.some(r=>r[2]>=100)","()=>RIDES.some(r=>r[6]!=null&&r[6]<8)","()=>RIDES.some(r=>r[7]==='train')"]:
        rep(a,a.replace("RIDES.some","okR().some"))
    rep("'Partir avant 8 h (validé dès le départ)'","'Partir avant 8 h et terminer ton tracé'")
    rep("'Terminer une sortie avant midi'","'Terminer ton tracé avant midi'")
    rep("Ils repartent à zéro le 1er du mois.</p>${ch}","Ils repartent à zéro le 1er du mois. Seules les sorties terminées comptent.</p>${ch}")
    # plus de validation au départ : défi en attente
    rep("nk:'',sb:startChal(startH)})","nk:'',sb:[],pend:startH<8&&!((CLAIM||{})[curYM()]||{}).early})")
    m=re.search(r"\$\{\(REC\.sb\|\|\[\]\)\.length\?`<div class=\\\"rbn\\\">.*?\)\.join\(''\)\}</div>`:''\}",s)
    if not m:
        # find by markers
        a=s.index("${(REC.sb||[]).length?`<div class=\"rbn\">");b=s.index(":''}",a)+4
        s=s[:a]+"${REC.pend?`<div class=\"rbn\"><div class=\"bl\"><i>⏱</i><span>Défi <b>Lève-tôt</b> en cours : termine ton tracé pour gagner +100 XP</span></div></div>`:''}"+s[b:]
    else:
        s=s[:m.start()]+"${REC.pend?`<div class=\"rbn\"><div class=\"bl\"><i>⏱</i><span>Défi <b>Lève-tôt</b> en cours : termine ton tracé pour gagner +100 XP</span></div></div>`:''}"+s[m.end():]
    # complétion de la sortie
    rep("(REC.plan&&REC.plan.rmode==='train')?'train':'']}","(REC.plan&&REC.plan.rmode==='train')?'train':'',(REC.plan?REC.km>=REC.plan.km*.9:REC.km>=10)]}")
    rep("PV=previewDone(recRide(def),SS);REC.pv=PV;","RR=recRide(def),PV=previewDone(RR,SS),NC=RR[8]===false?`<p class=\"warn2\" style=\"margin:10px 0 0\"><b>Tracé non terminé</b> (${REC.plan?Math.round(REC.km/REC.plan.km*100)+' % parcouru':'moins de 10 km'}) : les défis et badges ne sont pas validés. Va au bout de ton tracé pour les gagner.</p>`:'';REC.pv=PV;")
    rep("${bonusHTML((REC.sb||[]),[]).replace(/Défi validé :/g,'Défi validé au départ :')}","${NC}")
    # sync : sortie validée = terminée
    rep("(q.stops||[]).map(x=>[x[0],x[1]]),startH,q.mode==='train'?'train':''];","(q.stops||[]).map(x=>[x[0],x[1]]),startH,q.mode==='train'?'train':'',true];")
    open(p,'w',encoding='utf-8').write(s);print(f,'ok')
