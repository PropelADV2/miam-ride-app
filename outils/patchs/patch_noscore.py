import re
for f in ['accueil-velo.html','miam-ride-osm.html','introduction-miam-ride.html']:
    p='/mnt/user-data/outputs/'+f;s=open(p,encoding='utf-8').read()
    def rep(a,b):
        global s
        assert s.count(a)==1,(f,a[:70],s.count(a));s=s.replace(a,b)
    i=s.index("const tags=b=>{if(!S.prod)");j=s.index("\n",i)
    s=s[:i]+"const tags=b=>S.prod&&prodOf(b)?`<span class=\"pdl\">Propose : ${S.prod.toLowerCase()}</span>`:'';"+s[j:]
    rep("const srt=a=>a.sort((x,y)=>(S.prod?pScore(y)-pScore(x):0)||(y[6]-x[6])||(y[3]-x[3]));","const srt=a=>a.sort((x,y)=>(y[6]-x[6])||(y[3]-x[3]));")
    s=s.replace("les notes, avis, notes par produit et avantages partenaires sont fictifs","les produits proposés, notes, avis et avantages partenaires sont fictifs").replace("notes, avis, notes par produit et partenariats fictifs","produits proposés, notes, avis et partenariats fictifs")
    open(p,'w',encoding='utf-8').write(s)
# espace
p='/mnt/user-data/outputs/espace-boulangerie.html';s=open(p,encoding='utf-8').read()
a=s.index('<div class="box peach" style="margin:12px 0 0"><p class="sub" style="margin:0 0 6px;font-weight:600;color:var(--ink)">Ta place dans ton secteur');b=s.index('<button class="btn" id="save"')
s=s[:a]+'<div class="box peach" style="margin:12px 0 0"><p class="sub" style="margin:0 0 6px;font-weight:600;color:var(--ink)">Où tu apparaîtras</p><ul class="rk" id="rk"></ul><p class="sub" style="margin:6px 0 0;font-size:12px">Démonstration : l’ordre dans les résultats dépendra des notes laissées par les cyclistes après leur passage. Tant qu’il n’y en a pas, tu apparais avec les autres boulangeries du secteur qui proposent le produit.</p></div>\n      '+s[b:]
i=s.index("const PRODS=");j=s.index("const ME=")
s=s[:i]+"const PRODS=['Flan','Croissant','Pain au chocolat','Éclair','Tarte','Baguette tradition','Sandwich'],PRODX=['Mille-feuille','Chausson aux pommes','Macaron','Religieuse','Paris-Brest'];\n"+s[j:]
i=s.index("const ME='Aux Pains");j=s.index("rank();",i)
new='''const ALLP=PRODS.concat(PRODX),mine=new Set(['Flan','Croissant','Sandwich','Baguette tradition']);
function rank(){
 $('#menu').innerHTML=ALLP.map(x=>`<button type="button" aria-pressed="${mine.has(x)}">${x}</button>`).join('');
 $('#menu').querySelectorAll('button').forEach((b,i)=>b.onclick=()=>{const x=ALLP[i];mine.has(x)?mine.delete(x):mine.add(x);rank()});
 const L=ALLP.filter(p=>mine.has(p)).map(p=>`<li><b>${p}</b><span>dans les recherches « ${p.toLowerCase()} »</span></li>`);
 $('#rk').innerHTML=L.length?L.join(''):'<li><span>Coche au moins une spécialité pour apparaître dans les recherches par produit.</span></li>'}
'''
s=s[:i]+new+s[j:]
open(p,'w',encoding='utf-8').write(s)
