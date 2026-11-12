import json,math,re
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
src=open('t_dest2.py').read().split("with sync_playwright() as p:")[0]
src=src.replace('vers 22.html','vers 32.html')
exec(src);F='Miam ride osm - vers 32.html'
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

with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);ctx=b.new_context(viewport={'width':400,'height':860});pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/functions/v1/train-retour',srv);pg.route('**/overpass*/**',ovp3);pg.route('**/maps.mail.ru/**',ovp3);pg.route('**/photon.komoot.io/**',photon3);pg.route('**/api-adresse.data.gouv.fr/**',lambda r:r.fulfill(headers={'access-control-allow-origin':'*'},body='{"features":[]}'))
    pg.on('console',lambda m:print('CON',m.text[:150]));pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('mr_orskey','K')");pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1500)
    P="()=>S.loopG&&S.loopG.path&&S.loopG.path.length"
    # --- boucle
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(500)
    pg.wait_for_timeout(3000)
    print('GP',pg.evaluate("gPrepare.toString().slice(0,120)"),pg.evaluate("[!!S.loopG,S.loopG&&S.loopG.path&&S.loopG.path.length,S.gen]"))
    print('SEEN1',pg.evaluate("[S.seen&&S.seen.length,S.vary]"))
    print('boucle: bouton',pg.evaluate("[$('#regen').hidden,$('#regen').textContent]"),'km',pg.evaluate("Math.round(S.loopG.km)"))
    p1=pg.evaluate("S.loopG.path.map(p=>({lat:p.lat,lng:p.lng}))")
    pg.evaluate("document.querySelector('#regen').click()");pg.wait_for_timeout(500);pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(800)
    print('boucle 2: vary',pg.evaluate("S.vary"),'recouvrement',pg.evaluate("pathOverlap(S.loopG.path,S.seen[0])"),'km',pg.evaluate("Math.round(S.loopG.km)"),'seen',pg.evaluate("S.seen.length"),'gen',pg.evaluate("S.gen"),'bouton',pg.evaluate("$('#regen').hidden"))
    # --- vers un lieu
    pg.click('.mode[data-m="dest"]');pg.wait_for_timeout(300)
    print('dest: toggle Boucle/rapide',pg.evaluate("!!document.querySelector('#panel [data-f]')"),'| titre',pg.evaluate("$('#panel h2').textContent"),'| slider',pg.evaluate("!!document.querySelector('#km')"),'| fast',pg.evaluate("S.fast"))
    pg.fill('#to','Rambouillet');pg.wait_for_timeout(1200);pg.keyboard.press('Enter');pg.wait_for_timeout(1500)
    print('dest',pg.evaluate("S.dest&&S.dest.label"))
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(800)
    print('trajet 1: km',pg.evaluate("Math.round(S.loopG.km)"),'bouton',pg.evaluate("[$('#regen').hidden,$('#regen').textContent]"),'vary',pg.evaluate("S.vary"),'seen',pg.evaluate("S.seen.length"))
    pg.evaluate("document.querySelector('#regen').click()");pg.wait_for_timeout(500);pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(800)
    print('trajet 2: km',pg.evaluate("Math.round(S.loopG.km)"),'recouvrement',pg.evaluate("pathOverlap(S.loopG.path,S.seen[0])"),'via',pg.evaluate("!!S.loopG.via"),'seen',pg.evaluate("S.seen.length"),'ambiance',pg.evaluate("S.loopG.amb&&S.loopG.amb.met"))
    pg.evaluate("document.querySelector('#regen').click()");pg.wait_for_timeout(500);pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(800)
    print('trajet 3: km',pg.evaluate("Math.round(S.loopG.km)"),'rec/1',pg.evaluate("pathOverlap(S.loopG.path,S.seen[0])"),'rec/2',pg.evaluate("pathOverlap(S.loopG.path,S.seen[1])"))
    pg.screenshot(path='/tmp/v31_dest.png')
    print('despur',pg.evaluate("""async()=>{const o={lat:48.8,lng:2.1},P=[];for(let i=0;i<=40;i++)P.push({lat:o.lat,lng:o.lng+i*0.0004});for(let i=1;i<=20;i++)P.push({lat:o.lat+i*0.0002,lng:o.lng+0.016});for(let i=20;i>=0;i--)P.push({lat:o.lat+i*0.0002+0.000004,lng:o.lng+0.016});for(let i=41;i<=80;i++)P.push({lat:o.lat,lng:o.lng+i*0.0004});
      const spurW={lat:o.lat+0.004,lng:o.lng+0.016},okW={lat:o.lat,lng:o.lng+0.03};const r={km:50,path:P,mids:[okW,spurW]};
      const c0=RoutingORS.compute;let call=0;RoutingORS.compute=async(a,b,m)=>{call++;const Q=[];for(let i=0;i<=80;i++)Q.push({lat:o.lat,lng:o.lng+i*0.0004});return{km:49,path:Q,mids:m}};
      const x=await despur(o,o,r);RoutingORS.compute=c0;return {bt0:Math.round(btv(r)),btNew:Math.round(btv(x)),mids:x.mids.length,call,changed:x!==r}}"""))
    print('erreurs',errs)
