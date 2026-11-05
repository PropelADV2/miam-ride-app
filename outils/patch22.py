t=open('build_osm21.py').read()
def rp(a,b):
    global t
    assert t.count(a)==1,(a[:90],t.count(a)); t=t.replace(a,b)
t=t.replace("Miam ride osm - vers 21.html","Miam ride osm - vers 22.html")
a=t.index("async function trainSnap(g){"); b=t.index("{const d0=destSet;")
new=r"""async function trainSnap(g){osmToast('Recherche de la gare la plus proche…');let L=[];
 for(const r of [6,15,35,70]){try{L=await osmStations(g,r)}catch(e){osmToast('Gares indisponibles : '+e.message);return}if(L.length)break}
 if(!L.length){S.dest=null;S.trainAlt=null;osmToast('Aucune gare repérée dans cette région : essaie une autre ville');return}
 const A=L.map(s=>({s,d:hav(s,g)})).sort((x,y)=>x.d-y.d).slice(0,4);S.trainAlt=A.map(x=>Object.assign({dd:x.d},x.s));S.trainPlace=g.label;
 setTrainDest(S.trainAlt[0]);const d=S.trainAlt[0].dd;osmToast(S.trainAlt[0].name+(d>4?' : la plus proche de '+g.label.split(',')[0]+' (à '+Math.round(d)+' km)':''));drawAlt()}
function drawAlt(){const box=document.getElementById('tr_sel');if(!box||S.tdist||!S.trainAlt||!S.trainAlt.length)return;const place=(S.trainPlace||'ton lieu').split(',')[0];
 box.innerHTML='<p class="sub" style="margin:0 0 6px;font-weight:600">Gares proches de '+xe(place)+'</p>';
 S.trainAlt.forEach(s=>{const b=document.createElement('button');b.type='button';const sel=S.dest&&S.dest.label===s.name;b.setAttribute('aria-pressed',sel);b.textContent=s.name+' · à '+(s.dd<1?Math.round(s.dd*1000)+' m':String(Math.round(s.dd*10)/10).replace('.',',')+' km')+' de '+place;
  b.style.cssText='display:block;width:100%;text-align:left;margin:0 0 6px;padding:10px 12px;border:2px solid var(--ink);border-radius:14px;background:'+(sel?'var(--ink)':'#fff')+';color:'+(sel?'#fff':'var(--ink)')+';font:600 13px Poppins,sans-serif;cursor:pointer';
  b.onclick=()=>{setTrainDest(s);drawAlt()};box.appendChild(b)})}
"""
t=t[:a]+new+t[b:]
rp("else box.innerHTML='<p class=\"sub\">Tape une ville ou une gare dans « Où veux-tu aller ? » : on choisit la gare la plus proche (à moins de 4 km).</p>'+(S.dest&&S.dest.st?'<p class=\"sub\"><b>'+xe(S.dest.label)+'</b></p>':'')}",
   "else{box.innerHTML='<p class=\"sub\">Tape une ville ou une gare dans « Où veux-tu aller ? » : on te propose la gare la plus proche de ce lieu.</p>';if(S.trainAlt)drawAlt()}}")
rp("if(S.mode==='train'&&S.dest&&!S.dest.st||S.mode==='dest'&&S.dest&&S.dest.st){S.dest=null;","if(S.mode==='train'&&S.dest&&!S.dest.st||S.mode==='dest'&&S.dest&&S.dest.st){S.dest=null;S.trainAlt=null;")
open('build_osm22.py','w').write(t)
