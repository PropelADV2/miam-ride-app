# vers 34 : Overpass surchargé = plus de « zéro boulangerie » mis en mémoire
s=open('/mnt/user-data/outputs/Miam ride osm - vers 33.html').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(a[:70],s.count(a)); s=s.replace(a,b)
# la mémoire ignore (et efface) les zones sans boulangerie
rep("const BAKC={load(){try{return JSON.parse(OSMS.get('mr_bakc')||'[]')}catch(e){return[]}}","const BAKC={load(){try{return JSON.parse(OSMS.get('mr_bakc')||'[]').filter(z=>z.l&&z.l.length>=3)}catch(e){return[]}}")
rep(" add(c,r,list){const a=this.load()"," add(c,r,list){if(!list||list.length<3)return;const a=this.load()")
# réponse vide ou « remark: timed out » d'Overpass = échec, on réessaie (au lieu de croire qu'il n'y a rien)
A="const j=await res.json();return osmClean((j.elements||[]).map(osmPlace))"
i=s.index(A);s=s[:i]+"const j=await res.json();if(!(j.elements||[]).length&&((j.remark&&/error|timed out|memory/i.test(j.remark))||radiusM>=5000))throw new Error('Overpass surchargé : réponse vide');return osmClean((j.elements||[]).map(osmPlace))"+s[i+len(A):]
rep("async function osmEnsure(c,r){const fresh=","async function osmEnsure(c,r){if(!OSMC.list||!OSMC.list.length)OSMC.t=0;const fresh=")
open('/mnt/user-data/outputs/Miam ride osm - vers 34.html','w').write(s);print(len(s))
