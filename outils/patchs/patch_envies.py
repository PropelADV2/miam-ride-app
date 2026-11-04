import re,sys
for f in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+f
    s=open(p,encoding='utf-8').read()
    n=0
    def sub(old,new,cnt=1):
        global s,n
        assert s.count(old)>=1,(f,old[:50])
        s=s.replace(old,new);n+=1
    sub('<p class="sub" style="margin:0 0 8px">Filtre selon tes envies, puis choisis ta boulangerie.</p>\n      <div class="chips" id="food"></div>\n      <div class="chips" id="where" style="margin:8px 0 12px"></div>',
        '<p class="sub" style="margin:0 0 8px">Choisis ta boulangerie.</p>\n      <div class="chips" id="food" hidden></div>\n      <div class="chips" id="where" hidden></div>')
    s,k=re.subn(r'const tags=b=>.*\n','const tags=b=>\'\'; // envies masquées (données conservées)\n',s);assert k==1
    s,k=re.subn(r'const matches=b=>.*\n','const matches=b=>true; // filtre envies désactivé\n',s);assert k==1
    s,k=re.subn(r'function wish\(\)\{.*\n','function wish(){return \'\'}\n',s);assert k==1
    sub('foodUI();\n','// foodUI(); // envies masquées\n') if False else None
    open(p,'w',encoding='utf-8').write(s)
    print(f,'ok')
p='/mnt/user-data/outputs/espace-boulangerie.html'
s=open(p,encoding='utf-8').read()
old=s[s.index('      <h3 style="font-size:15px;margin-top:18px">Ce que tu proposes</h3>'):s.index('      <button class="btn" id="save"')]
s=s.replace(old,'      <div hidden>\n'+old+'      </div>\n')
open(p,'w',encoding='utf-8').write(s);print('espace ok')
