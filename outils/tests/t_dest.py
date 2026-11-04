import json,math
from playwright.sync_api import sync_playwright
F='Miam ride osm - vers 16.html'
def hav(a,b):
    R=6371;p=math.pi/180;dl=(b[1]-a[1])*p;dg=(b[0]-a[0])*p
    x=math.sin(dl/2)**2+math.cos(a[1]*p)*math.cos(b[1]*p)*math.sin(dg/2)**2;return 2*R*math.asin(math.sqrt(x))
seen={'orsDest':0}
def ors(route):
    b=json.loads(route.request.post_data);co=b['coordinates'];heavy=bool(b.get('elevation'));pts=[];L=0
    for i in range(len(co)-1):
        L+=hav(co[i],co[i+1])
        for k in range(20):
            t=k/20;pts.append([co[i][0]+(co[i+1][0]-co[i][0])*t,co[i][1]+(co[i+1][1]-co[i][1])*t,100])
    pts.append(co[-1]+[100]);n=len(pts);dist=L*1.3*1000;nb=int(n*.2)
    ex={'waytypes':{'values':[[0,nb,2],[nb,n-1,3]]},'surface':{'values':[[0,n-1,3]]}} if heavy else {}
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':[{'geometry':{'coordinates':pts},'properties':{'summary':{'distance':dist,'duration':dist/5},'extras':ex}}]}))
def ovp(route):
    els=[{'type':'node','id':i,'lat':48.70+0.02*(i%12),'lon':1.80+0.03*(i//12),'tags':{'name':'B%d'%i,'opening_hours':'Tu-Su 06:30-19:30'}} for i in range(120)]
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'elements':els}))
def photon(route):
    q=route.request.url.lower()
    f=[{'geometry':{'coordinates':[1.8315,48.6430]},'properties':{'name':'Gare de Rambouillet','city':'Rambouillet'}}] if 'rambouillet' in q else []
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':f}))
def ban(route):
    q=route.request.url.lower()
    f=[{'geometry':{'coordinates':[1.8315,48.6430]},'properties':{'label':'Rue de la Gare 78120 Rambouillet'}}] if 'rambouillet' in q else []
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':f}))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/overpass*/**',ovp);pg.route('**/maps.mail.ru/**',ovp);pg.route('**/photon.komoot.io/**',photon);pg.route('**/api-adresse.data.gouv.fr/**',ban)
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.removeItem('mr_bakc');localStorage.removeItem('mr_bstat')");pg.reload();pg.wait_for_timeout(500)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1200)
    pg.click('.mode[data-m="dest"]');pg.wait_for_timeout(300)
    # 1) pas de lieu : message clair
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_timeout(2500)
    print('sans lieu → toast :',pg.evaluate("(document.getElementById('osm_toast')||{}).textContent"),'| loopG',pg.evaluate("!!S.loopG"))
    # 2) saisie + suggestions
    pg.fill('#to','Rambouillet');pg.wait_for_timeout(900)
    print('suggestions :',pg.evaluate("[...document.querySelectorAll('#to_sug option')].map(o=>o.value)"))
    pg.evaluate("document.querySelector('#to').dispatchEvent(new Event('change',{bubbles:true}))");pg.wait_for_timeout(600)
    print('S.dest :',pg.evaluate("S.dest"))
    # 3) boucle via le lieu
    pg.evaluate("S.km=75");pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(500)
    r=pg.evaluate("({km:S.loopG.km,wp:S.loopG.waypoints.map(w=>[+w.lat.toFixed(3),+w.lng.toFixed(3)]),amb:S.loopG.amb&&S.loopG.amb.n,dest:!!S.loopG.dest,np:S.gen})")
    print('boucle via lieu : km %.1f'%r['km'],'waypoints',r['wp'],'candidats',r['amb'],'dest field',r['dest'])
    pg.evaluate("async()=>{S.picks=[ALL[0]];await gFinal()}") if False else None
    # 4) le plus rapide
    pg.evaluate("S.fast=true;S.gen=false;S.loopG=null;OSMC.key=null");pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=40000);pg.wait_for_timeout(500)
    r=pg.evaluate("({km:S.loopG.km,dest:S.loopG.dest,bk:baseKm(),n:ALL.length})")
    print('le plus rapide : km %.1f'%r['km'],'dest',r['dest'],'baseKm',r['bk'],'boulangeries',r['n'])
    pg.evaluate("S.picks=[ALL[0]]");fin=pg.evaluate("async()=>{await gFinal();const e=S.routeG.path[S.routeG.path.length-1];return[e.lat,e.lng,S.routeG.km]}")
    print('final : arrivée',[round(x,3) for x in fin[:2]],'km %.1f'%fin[2])
    print('erreurs',errs)
