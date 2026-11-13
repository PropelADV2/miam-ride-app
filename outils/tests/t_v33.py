import json,math,re
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
src=open('t_dest2.py').read().split("with sync_playwright() as p:")[0]
src=src.replace('vers 22.html','vers 33.html')
exec(src);F='Miam ride osm - vers 33.html'
STAT=[('Rambouillet',48.6430,1.8315),('Dourdan',48.5310,2.0100),('Saint-Quentin-en-Yvelines',48.7890,2.0460),('Épernon',48.6080,1.6770),('Plaisir-Grignon',48.8100,1.9500),('Chartres',48.4476,1.4813),('Châtelet',48.8584,2.3470),('Maintenon',48.5878,1.5791),('Épernon-Sud',48.5700,1.6600)]
QUERIES=[]
def ovp3(route):
    body=route.request.post_data or ''
    if 'railway' in body:
        els=[{'type':'node','id':i,'lat':la,'lon':lo,'tags':{'name':n,'railway':'station','network':'Transilien'}} for i,(n,la,lo) in enumerate(STAT)]
        els.append({'type':'node','id':99,'lat':48.80,'lon':2.13,'tags':{'name':'Métro X','railway':'station','station':'subway'}})
    else:
        els=[{'type':'node','id':i,'lat':48.70+0.02*(i%12),'lon':1.80+0.03*(i//12),'tags':{'name':'B%d'%i,'opening_hours':'Mo-Su 06:30-19:30'}} for i in range(120)]
        QUERIES.append(body)
        if 'amenity' in body: els+= [{'type':'node','id':500+i,'lat':48.70+0.02*(i%12)+0.001,'lon':1.80+0.03*(i//12)+0.001,'tags':{'name':'Café C%d'%i,'amenity':'cafe','opening_hours':'Mo-Su 07:00-20:00'}} for i in (36,48,60,61,72,73,74,85,86,87)]
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'elements':els}))
def photon3(route):
    q=route.request.url.lower()
    f=[{'geometry':{'coordinates':[1.8300,48.6420]},'properties':{'name':'Rambouillet','city':'Rambouillet'}}] if 'rambouillet' in q else ([{'geometry':{'coordinates':[1.7000,48.5500]},'properties':{'name':'Hanches','city':'Hanches'}}] if 'hanches' in q else [])
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':f}))
CALLS=[]
def srv(route):
    h={'access-control-allow-origin':'*','access-control-allow-headers':'*','access-control-allow-methods':'*','content-type':'application/json'}
    if route.request.method=='OPTIONS': route.fulfill(status=204,headers=h);return
    b=json.loads(route.request.post_data);CALLS.append(b)
    if abs(b['from']['lat']-48.53)<0.01: route.fulfill(headers=h,body=json.dumps({'ok':True,'trajets':[]}));return
    base=17*60+10+(0 if b['from']['lat']>48.7 else 25)
    T=[]
    for k,(dm,li) in enumerate([(0,'N'),(30,'N'),(60,'U'),(90,'N')]):
        T.append({'depart_gare':{'date':b['datetime'][:10],'min':base+dm},'arrivee':{'date':b['datetime'][:10],'min':base+dm+55},'duree_min':55,'correspondances':1 if li=='U' else 0,'lignes':[{'mode':'Train','ligne':li,'reseau':'Transilien'}]+([{'mode':'RER','ligne':'C','reseau':'RER'}] if li=='U' else [])})
    route.fulfill(headers=h,body=json.dumps({'ok':True,'trajets':T}))

import time
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);ctx=b.new_context(viewport={'width':400,'height':860});pg=ctx.new_page();errs=[];pg.on('console',lambda m:print('CON',m.text[:200]) if 'TUNNEL' not in m.text else 0);pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/functions/v1/train-retour',srv);pg.route('**/overpass*/**',ovp3);pg.route('**/maps.mail.ru/**',ovp3);pg.route('**/photon.komoot.io/**',photon3);pg.route('**/api-adresse.data.gouv.fr/**',lambda r:r.fulfill(headers={'access-control-allow-origin':'*'},body='{"features":[]}'))
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.setItem('mr_kind','cafe')");pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1500)
    # unit : backtrack
    print('backtrack aller-retour',pg.evaluate("""()=>{const o={lat:48.8,lng:2.1},P=[];for(let i=0;i<=40;i++)P.push({lat:o.lat+i*0.0002,lng:o.lng});for(let i=40;i>=0;i--)P.push({lat:o.lat+i*0.0002+0.000005,lng:o.lng});for(let i=0;i<30;i++)P.push({lat:o.lat,lng:o.lng+i*0.0003});return backtrack(P).m}"""),'m (attendu ~ 300)')
    print('backtrack boucle propre',pg.evaluate("""()=>{const P=[];for(let a=0;a<360;a+=3)P.push({lat:48.8+0.02*Math.sin(a*Math.PI/180),lng:2.1+0.03*Math.cos(a*Math.PI/180)});return backtrack(P).m}"""),'m (attendu 0)')
    print('backtrack croisement',pg.evaluate("""()=>{const P=[];for(let i=-30;i<=30;i++)P.push({lat:48.8+i*0.0002,lng:2.1});for(let i=-30;i<=30;i++)P.push({lat:48.8,lng:2.1+i*0.0003});return backtrack(P).m}"""),'m (attendu 0)')
    print('ERRS0',errs)
    print('trim impasse',pg.evaluate("""()=>{const o={lat:48.8,lng:2.1},P=[];for(let i=0;i<=40;i++)P.push({lat:o.lat,lng:o.lng+i*0.0004});for(let i=1;i<=20;i++)P.push({lat:o.lat+i*0.0002,lng:o.lng+0.016});for(let i=20;i>=0;i--)P.push({lat:o.lat+i*0.0002+0.000004,lng:o.lng+0.016});for(let i=41;i<=80;i++)P.push({lat:o.lat,lng:o.lng+i*0.0004});const t=trimSpurs(P);return {avant:P.length,apres:t.path.length,retire_m:Math.round(t.removedM),n:t.n}}"""))
    print('trim boucle propre',pg.evaluate("""()=>{const P=[];for(let a=0;a<=360;a+=2)P.push({lat:48.8+0.02*Math.sin(a*Math.PI/180),lng:2.1+0.03*Math.cos(a*Math.PI/180)});const t=trimSpurs(P);return {avant:P.length,apres:t.path.length,n:t.n}}"""))
    print('trim tour de pâté de maisons',pg.evaluate("""()=>{const o={lat:48.8,lng:2.1},P=[];for(let i=0;i<=20;i++)P.push({lat:o.lat,lng:o.lng+i*0.0004});for(let i=1;i<=20;i++)P.push({lat:o.lat+i*0.0003,lng:o.lng+0.008});for(let i=19;i>=0;i--)P.push({lat:o.lat+0.006,lng:o.lng+i*0.0004});for(let i=19;i>=0;i--)P.push({lat:o.lat+i*0.0003,lng:o.lng});const t=trimSpurs(P);return {avant:P.length,apres:t.path.length,n:t.n}}"""))
    t0=time.time();pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=25000);pg.wait_for_timeout(800)
    print('boucle café: %.1f s'%(time.time()-t0),'| kind',pg.evaluate("S.kind"),'| bt',pg.evaluate("Math.round(btv(S.loopG))"),'| cafés',pg.evaluate("OSMC.list.filter(p=>p.kind==='cafe').length"),'| boulangeries',pg.evaluate("OSMC.list.filter(p=>p.kind!=='cafe').length"))
    big=[q for q in QUERIES if 'amenity' in q and 'around:2' in q]
    print('requêtes :',len(QUERIES),'| avec cafés :',sum('amenity' in q for q in QUERIES),'| café + rayon>=10km :',sum(1 for q in QUERIES if 'amenity' in q and any(int(x)>=10000 for x in re.findall(r'around:(\d+)',q))))
    print('erreurs',errs)
