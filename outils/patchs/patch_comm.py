import sys
def rep(s,a,b,n=1):
    assert s.count(a)==n,(a[:60],s.count(a)); return s.replace(a,b)
for f in sys.argv[1:]:
    s=open(f).read()
    s=rep(s,"const prodOf=(b,p)=>(SPEC[b[0]]||{})[p||S.prod]||null,pScore=(b,p)=>{const r=prodOf(b,p);return r?(r[0]*r[1]+4*5)/(r[1]+5):0};",
"""const REV_MIN=5,CONF_MIN=3,FEM=['Tarte','Baguette tradition','Religieuse','Chausson aux pommes'];
const simOn=()=>{try{return localStorage.getItem('mr_sim')==='1'}catch(e){return false}};
const decl=(b,p)=>!!(SPEC[b[0]]||{})[p];
/* Avis des cyclistes sur un produit. En démo : tes avis + (option) des avis simulés tirés de SPEC. En vrai : tous les avis validés par QR. */
function comm(b,p){const mine=REVS.filter(r=>r.b===b[0]&&r.p===p),sp=simOn()?(SPEC[b[0]]||{})[p]:null,n=mine.length+(sp?sp[1]:0),sum=mine.reduce((a,r)=>a+r.s,0)+(sp?sp[0]*sp[1]:0);return{n,avg:n?sum/n:0}}
/* Un produit est proposé s'il est déclaré par la boulangerie, ou confirmé par au moins CONF_MIN avis de cyclistes. */
const prodOf=(b,p)=>{p=p||S.prod;if(!p)return null;const c=comm(b,p);return decl(b,p)||c.n>=CONF_MIN?[c.avg,c.n]:null};
/* Score pondéré, seulement à partir de REV_MIN avis (sinon 0 = pas classé). */
const pScore=(b,p)=>{const r=prodOf(b,p);return r&&r[1]>=REV_MIN?(r[0]*r[1]+4*5)/(r[1]+5):0};""")
    s=rep(s,"const bestOf=p=>p?BAK.filter(b=>prodOf(b,p)).sort((x,y)=>pScore(y,p)-pScore(x,p))[0]||null:null;","const bestOf=p=>p?BAK.filter(b=>pScore(b,p)>0).sort((x,y)=>pScore(y,p)-pScore(x,p))[0]||null:null;")
    s=rep(s,"const srt=a=>a.sort((x,y)=>(y[6]-x[6])||(y[3]-x[3]));","const srt=a=>a.sort((x,y)=>(y[6]-x[6])||(S.prod?pScore(y,S.prod)-pScore(x,S.prod):0)||(y[3]-x[3]));")
    s=rep(s,"const tags=b=>{if(!S.prod||!prodOf(b))return'';const m=myRev(b[0],S.prod);return `<span class=\"pdl\">Propose : ${S.prod.toLowerCase()}${m?` · ton avis : ${m.s}/5`:''}</span>`};",
"""const tags=b=>{if(!S.prod||!prodOf(b))return'';const p=S.prod,c=comm(b,p),m=myRev(b[0],p),
 src=decl(b,p)?(c.n>=CONF_MIN?'confirmé par les cyclistes':''):'ajouté par les cyclistes',
 note=c.n>=REV_MIN?` · ${fr1(c.avg)}/5 (${c.n} avis)`:(c.n?' · pas encore assez d’avis':''),
 best=bestOf(p)===b?`<span class="pdl best">${FEM.includes(p)?'Meilleure':'Meilleur'} ${p.toLowerCase()} du secteur</span>`:'';
 return best+`<span class="pdl">Propose : ${p.toLowerCase()}${note}${src?` · ${src}`:''}${m?` · ton avis : ${m.s}/5`:''}</span>`};""")
    s=rep(s,"REVS.push({b:st.n,p:prod,s:stars,d:todayIso()});saveRevs();","const _i=REVS.findIndex(r=>r.b===st.n&&r.p===prod&&r.d===todayIso()),_new=_i<0;if(_new)REVS.push({b:st.n,p:prod,s:stars,d:todayIso()});else REVS[_i].s=stars;saveRevs();")
    s=rep(s,"Ton avis sur ${prod.toLowerCase()} est enregistré. +${REVXP} XP.","Ton avis sur ${prod.toLowerCase()} est enregistré : il compte pour la note et pour confirmer l’offre de ${st.n}. ${_new?'+'+REVXP+' XP.':'Avis du jour mis à jour, sans nouvelle XP.'}")
    s=rep(s,'<div class="row"><label for="f_near">','<div class="row"><label for="f_sim">Démo : avis simulés d’autres cyclistes</label><select id="f_sim"><option value="0">Désactivés</option><option value="1">Activés</option></select></div><div class="row"><label for="f_near">')
    s=rep(s,"profInit();(()=>{const n=$('#f_near');","profInit();(()=>{const s=$('#f_sim');if(s){s.value=simOn()?'1':'0';s.onchange=()=>{try{localStorage.setItem('mr_sim',s.value)}catch(x){}if($('#res').classList.contains('on'))showRes();if(typeof xSheet==='function')xSheet()}}})();(()=>{const n=$('#f_near');")
    s=rep(s,'<div id="xss"></div>','<div id="xss"></div><div id="xpr"></div>')
    s=rep(s," const ph=$('#xph');",""" const pr=$('#xpr');if(par){const all=PRODS.concat(PRODX).filter(x=>prodOf(b,x)).sort((x,y)=>(x===XM.prod?-1:y===XM.prod?1:0)||pScore(b,y)-pScore(b,x));
 pr.innerHTML=all.length?`<p class="xpt">Produits et avis des cyclistes</p><div>${all.map(x=>{const c=comm(b,x);return `<span class="xtg">${x}${c.n>=REV_MIN?` · ${fr1(c.avg)}/5 (${c.n})`:''}</span>`}).join('')}</div><p class="xpn">${simOn()?'Avis simulés pour la démo. ':''}Une note s’affiche à partir de ${REV_MIN} avis ; un produit est confirmé à partir de ${CONF_MIN} avis.</p>`:''}else pr.innerHTML='';
 const ph=$('#xph');""")
    s=rep(s,'#xgo{','.pdl.best{background:var(--yellow);font-weight:800;display:inline-block;margin-bottom:3px}\n#xgo{')
    open(f,'w').write(s);print('ok',f)
