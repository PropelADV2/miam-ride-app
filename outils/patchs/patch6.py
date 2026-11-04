import re
VER='''const VER={"Giant|Propel Advanced":["Advanced 0","Advanced 1","Advanced 2","Pro 0 Di2","Pro 1 Di2","Pro 1 AXS"],"Giant|TCR Advanced":["SL 1 Di2","Pro 0 Di2","Pro 0 AXS","Pro 1 Di2"]};
'''
ROWS='<div class="row" id="rvv" hidden><label for="f_vv">Version</label><select id="f_vv" data-f="f_vv"></select></div><div class="row" id="rvvx" hidden><label for="f_vvx">Version (facultatif)</label><input type="text" id="f_vvx" data-f="f_vvx" placeholder="Ex. : Pro 1 Di2" autocomplete="off" maxlength="30"></div>'
TAIL=''' const V=$('#f_vv'),VX=$('#f_vvx');
 const vers=(keep)=>{const has=B.value!=='Choisir…'&&M.value!=='Choisir…',L=VER[B.value+'|'+M.value]||[];$('#rvv').hidden=!(has&&L.length);V.innerHTML=bkOpt(['Choisir…',...L,'Autre version…']);if(keep&&[...V.options].some(o=>o.value===keep))V.value=keep;$('#rvvx').hidden=!has||(L.length>0&&V.value!=='Autre version…')};
 vers(F.f_vv);
 const save=()=>{F.f_vt=T.value;F.f_vm=B.value;F.f_vmo=M.value;F.f_vv=V.value;persist()};
 T.onchange=()=>{brands();B.value='Choisir…';models();showCust();vers();save()};
 B.onchange=()=>{models();M.value='Choisir…';if(B.value==='Autre marque…'){M.innerHTML=bkOpt(['Autre modèle…']);M.value='Autre modèle…'}showCust();vers();save()};
 M.onchange=()=>{showCust();vers();save()};
 V.onchange=()=>{vers(V.value);save()}}
'''
for fn in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+fn;s=open(p,encoding='utf-8').read()
    def rep(a,b,rx=False):
        global s
        if rx:
            s,k=re.subn(a,lambda m:b,s,count=1,flags=re.S);assert k==1,(fn,a[:50])
        else:
            assert a in s,(fn,a[:60]);s=s.replace(a,b,1)
    rep('<div class="row"><label for="f_vp">',ROWS+'<div class="row"><label for="f_vp">')
    rep("function bikeLabel(){",VER+"function bikeLabel(){")
    rep(r"return \[b==='Choisir…'\?'':b,m==='Choisir…'\?'':m\]\.filter\(x=>x&&x\.trim\(\)\)\.join\(' '\)\}","const vv=v('f_vv')==='Autre version…'?v('f_vvx'):(v('f_vv')==='Choisir…'?v('f_vvx'):v('f_vv'));return [b==='Choisir…'?'':b,m==='Choisir…'?'':m,vv==='Choisir…'?'':vv].filter(x=>x&&x.trim()).join(' ')}",True)
    rep(r" const save=\(\)=>\{F\.f_vt.*?M\.onchange=\(\)=>\{showCust\(\);save\(\)\}\}\n",TAIL,True)
    open(p,'w',encoding='utf-8').write(s)
print('ok')
