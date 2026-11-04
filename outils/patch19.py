t=open('build_osm18.py').read()
def rp(a,b):
    global t
    assert t.count(a)==1,(a[:80],t.count(a)); t=t.replace(a,b)
t=t.replace("Miam ride osm - vers 18.html","Miam ride osm - vers 19.html")
anchor="rep('const res=await this.compute(c,c,items.map(x=>x.p));res.stops=stops;return res}','const res=await this.compute(c,loop.dest||c,items.map(x=>x.p));res.stops=stops;return res}')"
add=r"""
rep("const[lo,hi]=RULES.win[n][j],v=((ALL.indexOf(b)%5)-2)*.012,p=","const[lo,hi]=RULES.win[n][j];if(b&&b[9]&&b[9].f!=null){const q=Math.min(1,Math.max(0,b[9].f));return{km:Math.round(km*q),pct:Math.round(q*100)}}const v=((ALL.indexOf(b)%5)-2)*.012,p=")
rep("let base=BAK.filter(b=>!used.includes(b)),over=null,hw=false;","let base=(typeof bkWin==='function'?bkWin:(a=>a))(BAK.filter(b=>!used.includes(b)),j),over=null,hw=false;")
rep("(y[3]-x[3]));","(y[3]-x[3])||(typeof bkOrd==='function'?bkOrd(x,y):0));")"""
rp(anchor,anchor+add)
code=r"""/* ---------- position réelle de chaque boulangerie sur le tracé : fenêtres de pause respectées ---------- */
const _cumP=new WeakMap();
function pathFrac(path,p){let c=_cumP.get(path);if(!c){c=[0];for(let i=1;i<path.length;i++)c.push(c[i-1]+hav(path[i-1],path[i]));_cumP.set(path,c)}return c[nearestIdx(path,p).i]/(c[c.length-1]||1)}
{const g0=gTuple;gTuple=function(p,path){const r=g0.apply(this,arguments);if(osmOn()&&path&&path.length>1&&r[9])r[9].f=pathFrac(path,p);return r}}
function bkWin(list,j){if(!osmOn()||!S.np||!RULES.win[S.np]||!RULES.win[S.np][j])return list;const[lo,hi]=RULES.win[S.np][j];
 for(const tol of [0.03,0.12]){const L=list.filter(b=>b[9]&&b[9].f!=null&&b[9].f>=lo-tol&&b[9].f<=hi+tol);if(L.length)return L}return list}
function bkOrd(x,y){if(!osmOn())return 0;const r={v:0,r:1,n:2,x:3},sx=r[bStatT(x)]-r[bStatT(y)];if(sx)return sx;const w=RULES.win[S.np]&&RULES.win[S.np][Math.min(S.active||0,S.np-1)];if(!w)return 0;const m=(w[0]+w[1])/2,fx=x[9]&&x[9].f!=null?Math.abs(x[9].f-m):9,fy=y[9]&&y[9].f!=null?Math.abs(y[9].f-m):9;return fx-fy}
"""
rp("/* ---------- validation des boulangeries (Profil › Compte) ---------- */",code+"/* ---------- validation des boulangeries (Profil › Compte) ---------- */")
open('build_osm19.py','w').write(t)
