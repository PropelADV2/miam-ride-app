import re,json
CAT={
"Route":{
"3T":"Strada|Strada Italia","Basso":"Diamante","Bianchi":"Specialissima|Oltre RC|Aria|Sprint","BMC":"Teammachine R|Roadmachine|Timemachine","Boardman":"SLR 9.0","Canyon":"Ultimate|Aeroad|Endurace","Cannondale":"SuperSix EVO|CAAD13|Synapse","Cervélo":"S5|R5|Caledonia","Colnago":"V5Rs|Y1Rs|C68","Cube":"Attain|Agree|Litening","Decathlon (Triban)":"RC 120|RC 500|RC 520","Factor":"O2 VAM|Ostro VAM|One","Focus":"Izalco Max|Paralane","Fuji":"Transonic|Sportif","Giant":"TCR Advanced|TCR Advanced SL|Propel Advanced|Defy Advanced|Contend","Lapierre":"Xelius SL|Pulsium|Aircode DRS","Look":"795 Blade RS|785 Huez","Merida":"Scultura|Reacto","Nakamura":"Century 350|Century Team","Orbea":"Orca|Avant","Pinarello":"Dogma F|Prince","Ridley":"Noah|Helium|Fenix","Scott":"Addict RC|Foil RC|Speedster","Specialized":"Tarmac SL8|Aethos|Roubaix|Allez|Venge","Trek":"Madone|Émonda|Domane","Van Rysel":"RCR|EDR|NCR","Wilier":"Filante SLR|Cento10 SL|Zero SLR"},
"Gravel":{
"Bianchi":"Impulso","BMC":"URS","Canyon":"Grizl|Grail","Cannondale":"Topstone|SuperX","Cervélo":"Aspero","Cube":"Nuroad","Decathlon (Triban)":"GRVL 500|GRVL 520","Focus":"Atlas","Fuji":"Jari","Giant":"Revolt|Revolt Advanced","Lapierre":"Crosshill","Merida":"Silex","Orbea":"Terra","Ridley":"Kanzo|Kanzo Fast","Salsa":"Warbird","Santa Cruz":"Stigmata","Scott":"Addict Gravel|Speedster Gravel","Specialized":"Diverge|Crux","Trek":"Checkpoint","Van Rysel":"GRVL","Wilier":"Jena|Rave SLR"},
"VTT":{
"BMC":"Fourstroke|Twostroke","Cannondale":"Scalpel|Habit","Canyon":"Lux|Neuron|Spectral","Commencal":"Meta|Supreme","Cube":"Reaction|Stereo","Focus":"Jam|Raven","Giant":"Anthem|Trance|Talon","Lapierre":"Spicy|XR","Merida":"Big Nine|One-Twenty|Ninety-Six","Mondraker":"Podium|Foxy","Orbea":"Oiz|Occam","Decathlon (Rockrider)":"ST 100|ST 500|ST 900","Santa Cruz":"Blur|Hightower","Scott":"Spark|Scale|Genius","Specialized":"Epic|Epic 8|Stumpjumper|Chisel|Rockhopper","Trek":"Supercaliber|Top Fuel|Fuel EX|Procaliber","YT":"Izzo|Capra"}}
CATJ=json.dumps({t:{b:m.split('|') for b,m in d.items()} for t,d in CAT.items()},ensure_ascii=False,separators=(',',':'))
n=sum(len(v.split('|')) for d in CAT.values() for v in d.values());nb=len({b for d in CAT.values() for b in d})
print('modèles',n,'marques',nb)
JS='''
const CAT='''+CATJ+''';
const bkOpt=a=>a.map(x=>`<option>${x}</option>`).join('');
function bikeLabel(){const v=id=>($('#'+id)||{value:''}).value,b=v('f_vm')==='Autre marque…'?v('f_vmx'):v('f_vm'),m=v('f_vmo')==='Autre modèle…'?v('f_vmox'):v('f_vmo');return [b==='Choisir…'?'':b,m==='Choisir…'?'':m].filter(x=>x&&x.trim()).join(' ')}
function bikeInit(){const T=$('#f_vt'),B=$('#f_vm'),M=$('#f_vmo'),F=PROF.f;if(!T||!B||!M)return;
 T.innerHTML=bkOpt(Object.keys(CAT));T.value=CAT[F.f_vt]?F.f_vt:'Route';
 const brands=()=>{const t=T.value;B.innerHTML=bkOpt(['Choisir…',...Object.keys(CAT[t]),'Autre marque…'])},models=()=>{const b=B.value,t=T.value;M.innerHTML=bkOpt(['Choisir…',...((CAT[t]||{})[b]||[]),'Autre modèle…']);$('#rvmo').hidden=b==='Choisir…';},cust=()=>{$('#rvmx').hidden=B.value!=='Autre marque…';$('#rvmox').hidden=!(M.value==='Autre modèle…'||B.value==='Autre marque…'&&!$('#rvmo').hidden&&false)};
 const showCust=()=>{$('#rvmx').hidden=B.value!=='Autre marque…';$('#rvmox').hidden=M.value!=='Autre modèle…'};
 brands();B.value=[...B.options].some(o=>o.value===F.f_vm)?F.f_vm:'Choisir…';models();M.value=[...M.options].some(o=>o.value===F.f_vmo)?F.f_vmo:'Choisir…';showCust();
 const save=()=>{F.f_vt=T.value;F.f_vm=B.value;F.f_vmo=M.value;persist()};
 T.onchange=()=>{brands();B.value='Choisir…';models();showCust();save()};
 B.onchange=()=>{models();M.value='Choisir…';if(B.value==='Autre marque…'){M.innerHTML=bkOpt(['Autre modèle…']);M.value='Autre modèle…'}showCust();save()};
 M.onchange=()=>{showCust();save()}}
'''
ROWS=('<div class="row"><label for="f_vt">Type</label><select id="f_vt" data-f="f_vt"></select></div>'
 '<div class="row"><label for="f_vm">Marque</label><select id="f_vm" data-f="f_vm"></select></div>'
 '<div class="row" id="rvmx" hidden><label for="f_vmx">Nom de la marque</label><input type="text" id="f_vmx" data-f="f_vmx" placeholder="Ex. : Marque" autocomplete="off"></div>'
 '<div class="row" id="rvmo" hidden><label for="f_vmo">Modèle</label><select id="f_vmo" data-f="f_vmo"></select></div>'
 '<div class="row" id="rvmox" hidden><label for="f_vmox">Nom du modèle</label><input type="text" id="f_vmox" data-f="f_vmox" placeholder="Ex. : Modèle" autocomplete="off"></div>')
for fn in ['accueil-velo.html','miam-ride-osm.html']:
    p='/mnt/user-data/outputs/'+fn;s=open(p,encoding='utf-8').read()
    def rep(a,b,rx=False):
        global s
        if rx:
            s,k=re.subn(a,lambda m:b,s,count=1,flags=re.S);assert k==1,(fn,a[:50])
        else:
            assert a in s,(fn,a[:60]);s=s.replace(a,b,1)
    rep(r'<div class="row"><label for="f_vt">.*?</select></div><div class="row"><label for="f_vm">.*?</div><div class="row"><label for="f_vmo">.*?</div>',ROWS,True)
    rep("Ton vélo réel. Il sert pour les itinéraires","Catalogue des principales marques et modèles (pas exhaustif) : choisis « Autre » si le tien manque. Ton vélo réel sert pour les itinéraires")
    rep("function openSum(){",JS+"function openSum(){")
    rep("$('#f_vm')&&($('#f_vm').value||$('#f_vmo').value)?' · '+[$('#f_vm').value,$('#f_vmo').value].filter(Boolean).join(' '):''","bikeLabel()?' · '+bikeLabel():''")
    rep("profInit();","profInit();bikeInit();")
    open(p,'w',encoding='utf-8').write(s)
print('ok')
