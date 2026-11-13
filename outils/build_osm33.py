# vers 33 : les impasses (aller-retour sur une même rue) sont retirées du tracé final
s=open('/mnt/user-data/outputs/Miam ride osm - vers 32.html').read()
JS=r"""<script id="v33">
/* ===== vers 33 : on ne garde pas les culs-de-sac ===== */
/* un cul-de-sac = le tracé s'éloigne puis revient par la même rue : on coupe l'aller-retour et on repart du carrefour */
function trimSpurs(P){if(!P||P.length<8)return{path:P,removedM:0,n:0};
 const seg=(a,b)=>{let m=0;for(let k=a+1;k<=b;k++)m+=hav(P[k-1],P[k])*1000;return m};
 const retrace=(i,j)=>{const mid=Math.floor((i+j)/2),B=[];for(let k=mid;k<=j;k+=2)B.push(P[k]);if(!B.length)return false;let n=0,t=0;
  for(let k=i;k<mid;k+=2){t++;if(B.some(q=>hav(P[k],q)*1000<30))n++}return t>0&&n/t>=0.85};
 const out=[];let i=0,rm=0,n=0;
 while(i<P.length){out.push(P[i]);let jump=-1,far=0;
  for(let j=i+1;j<Math.min(P.length,i+700);j++){const d=hav(P[i],P[j])*1000;if(d>far)far=d;if(far>1500)break;
   if(far>40&&d<25&&j>i+3&&retrace(i,j)){jump=j;break}}
  if(jump>0){rm+=seg(i,jump);n++;i=jump}else i++}
 return{path:out,removedM:rm,n}}
function trimRoute(R){if(!R||!R.path)return R;const t=trimSpurs(R.path);if(t.n){R.path=t.path;R.km=Math.max(0,R.km-t.removedM/1000);R.trim=t.n;R.bt=null}return R}
{const g=gPrepare;gPrepare=async function(){const r=await g.apply(this,arguments);try{if(S.loopG)trimRoute(S.loopG)}catch(e){}return r}}
{const g=gFinal;gFinal=async function(){const r=await g.apply(this,arguments);try{if(S.routeG){trimRoute(S.routeG);S.gKm=S.routeG.km}}catch(e){}return r}}
</script>
"""
i=s.rindex("</body>");s=s[:i]+JS+s[i:]
open('/mnt/user-data/outputs/Miam ride osm - vers 33.html','w').write(s);print(len(s))
