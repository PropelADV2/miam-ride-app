t=open('build_osm19.py').read()
def rp(a,b):
    global t
    assert t.count(a)==1,(a[:80],t.count(a)); t=t.replace(a,b)
t=t.replace("Miam ride osm - vers 19.html","Miam ride osm - vers 20.html")
rp("zoneApply=function(tu){if(osmOn()){tu=tu.filter(","zoneApply=function(tu){if(osmOn()){S.bkc={corr:tu.length};tu=tu.filter(")
code=r"""/* ---------- contrôle : où passent les boulangeries ---------- */
function osmCnt(){if(!osmOn()||!S.gen||!S.np||!$('#stats'))return;let e=document.getElementById('osm_cnt');
 if(!e){e=document.createElement('p');e.id='osm_cnt';e.className='sub';e.style.cssText='font-size:12px;margin:0 0 6px';(document.getElementById('osm_dest')||document.getElementById('osm_amb')||$('#stats')).after(e)}
 const tot=(OSMC.list||[]).length,corr=S.bkc?S.bkc.corr:0,j=Math.min(S.active||0,S.np-1),w=RULES.win[S.np]&&RULES.win[S.np][j];
 const inw=w?BAK.filter(b=>b[9]&&b[9].f!=null&&b[9].f>=w[0]-0.03&&b[9].f<=w[1]+0.03):BAK.slice(),op=inw.filter(b=>{try{return hState(b,j)!=='closed'}catch(x){return true}});
 e.textContent='Boulangeries : '+tot+' dans OpenStreetMap · '+corr+' le long du tracé · '+BAK.length+' après filtres · '+inw.length+' dans la fenêtre de la pause '+(j+1)+' · '+op.length+' ouvertes à ton heure'+(tot===0?' — OpenStreetMap n’a rien renvoyé pour cette zone':'')}
{const o0=osmStats;osmStats=function(){const r=o0.apply(this,arguments);try{osmCnt()}catch(e){}return r}}
"""
rp("/* ---------- validation des boulangeries (Profil › Compte) ---------- */",code+"/* ---------- validation des boulangeries (Profil › Compte) ---------- */")
open('build_osm20.py','w').write(t)
