import re
f='/mnt/user-data/outputs/espace-boulangerie.html'
s=open(f,encoding='utf-8').read()
src=open('/mnt/user-data/outputs/accueil-velo.html',encoding='utf-8').read()
i=src.index("const PRODS=");j=src.index("const prodOf=")
data=src[i:j]
# HTML
a=s.index('      <div hidden>\n      <h3 style="font-size:15px;margin-top:18px">Ce que tu proposes</h3>')
b=s.index('<button class="btn" id="save"')
html='''      <h3 style="font-size:15px;margin-top:18px">Tes spécialités</h3>
      <label>Coche ce que tu fais de mieux. Les cyclistes qui cherchent un produit (un flan, un éclair…) voient d’abord les boulangeries les mieux notées pour ce produit.</label>
      <div class="chk" id="menu"></div>
      <div class="box peach" style="margin:12px 0 0"><p class="sub" style="margin:0 0 6px;font-weight:600;color:var(--ink)">Ta place dans ton secteur</p><ul class="rk" id="rk"></ul><p class="sub" style="margin:6px 0 0;font-size:12px">Classement fictif de démonstration. En vrai, il viendra des notes laissées par les cyclistes après leur passage.</p></div>
      '''
s=s[:a]+html+s[b:]
# CSS
s=s.replace('.chk button[aria-pressed="true"]{background:var(--yellow)}','.chk button[aria-pressed="true"]{background:var(--yellow)}\n.rk{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}.rk li{display:flex;justify-content:space-between;gap:10px;font-size:13px}.rk li b{font-weight:600}.rk li span{color:var(--muted);text-align:right}.rk .top{color:var(--ink);font-weight:700}',1)
# JS
c=s.index("const MENU=");d=s.index("chips('#menu',MENU);chips('#where',WH);")+len("chips('#menu',MENU);chips('#where',WH);")
js=data+'''const ME='Aux Pains de la Ferme',ALLP=PRODS.concat(PRODX),mine=new Set(Object.keys(SPEC[ME]));
const sc=(n,p)=>{const r=SPEC[n][p];return r?(r[0]*r[1]+20)/(r[1]+5):0};
function rank(){
 $('#menu').innerHTML=ALLP.map(x=>`<button type="button" aria-pressed="${mine.has(x)}">${x}</button>`).join('');
 $('#menu').querySelectorAll('button').forEach((b,i)=>b.onclick=()=>{const x=ALLP[i];mine.has(x)?mine.delete(x):mine.add(x);rank()});
 const L=ALLP.filter(p=>mine.has(p)).map(p=>{const r=SPEC[ME][p];if(!r)return `<li><b>${p}</b><span>pas encore d’avis : tu passes après les boulangeries notées</span></li>`;
  const names=Object.keys(SPEC).filter(n=>SPEC[n][p]).sort((x,y)=>sc(y,p)-sc(x,p)),k=names.indexOf(ME)+1;
  return `<li><b>${p}</b><span class="${k===1?'top':''}">${r[0].toFixed(1).replace('.',',')}/5 · ${r[1]} avis · ${k===1?'1re place':k+'e sur '+names.length}</span></li>`});
 $('#rk').innerHTML=L.length?L.join(''):'<li><span>Coche au moins une spécialité pour apparaître dans les recherches par produit.</span></li>'}
rank();'''
s=s[:c]+js+s[d:]
open(f,'w',encoding='utf-8').write(s)
