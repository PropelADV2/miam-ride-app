# vers 36 : cafés mis de côté (filtre masqué, on ne cherche que les boulangeries) ; le code reste en place
s=open('/mnt/user-data/outputs/Miam ride osm - vers 35.html').read()
JS="""<script id="v36">
/* ===== vers 36 : cafés en pause. Pour les réactiver : CAFES_ON=true ===== */
const CAFES_ON=false;
if(!CAFES_ON){S.kind='boulangerie';try{OSMS.set('mr_kind','boulangerie')}catch(e){}
 kindMount=function(){const w=document.getElementById('kindw');if(w)w.remove()};kindMount();try{render()}catch(e){}}
</script>
"""
i=s.rindex("</body>");s=s[:i]+JS+s[i:]
open('/mnt/user-data/outputs/Miam ride osm - vers 36.html','w').write(s);print(len(s))
