import json,math,sys
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'Miam ride osm - vers 12.html'
calls={'ovp':0,'ors':0,'heavy':0,'avoid':0}
def hav(a,b):
    R=6371;p=math.pi/180;dl=(b[1]-a[1])*p;dg=(b[0]-a[0])*p
    x=math.sin(dl/2)**2+math.cos(a[1]*p)*math.cos(b[1]*p)*math.sin(dg/2)**2;return 2*R*math.asin(math.sqrt(x))
def ors(route):
    calls['ors']+=1;b=json.loads(route.request.post_data);co=b['coordinates'];heavy=bool(b.get('elevation'))
    av=b.get('options',{}).get('avoid_polygons')
    if heavy: calls['heavy']+=1
    if av: calls['avoid']+=1
    pts=[];L=0
    for i in range(len(co)-1):
        L+=hav(co[i],co[i+1])
        for k in range(20):
            t=k/20;pts.append([co[i][0]+(co[i+1][0]-co[i][0])*t,co[i][1]+(co[i+1][1]-co[i][1])*t,100+8*math.sin(len(pts)/4)])
    pts.append(co[-1]+[100]);n=len(pts);dist=L*1.3*1000
    busy=0.12+0.4*abs(math.sin(co[1][0]*900))   # part de routes principales selon la forme de la boucle
    if av: busy*=0.45
    nb=int(n*busy);ex={'waytypes':{'values':[[0,nb,2],[nb,n-1,3]]},'surface':{'values':[[0,n-1,3]]}} if heavy else {}
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':[{'geometry':{'coordinates':pts},'properties':{'summary':{'distance':dist,'duration':dist/5},'extras':ex}}]}))
def ovp(route):
    calls['ovp']+=1
    els=[{'type':'node','id':i,'lat':48.74+0.02*(i%12),'lon':1.98+0.03*(i//12),'tags':{'name':'B%d'%i}} for i in range(60)]
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'elements':els}))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/overpass*/**',ovp);pg.route('**/maps.mail.ru/**',ovp)
    pg.goto('file:///mnt/user-data/outputs/'+F);pg.wait_for_timeout(600)
    pg.evaluate("localStorage.setItem('mr_orskey','K');localStorage.removeItem('mr_osm');localStorage.removeItem('mr_bakc')");pg.reload();pg.wait_for_timeout(600)
    print('osmOn par défaut',pg.evaluate("osmOn()"))
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(1500)
    for i in range(3):
        for k in calls: calls[k]=0
        pg.evaluate(f"PROF.amb={i};S.gen=false;S.loopG=null;S.routeG=null;OSMC.key=null")
        pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&S.loopG.amb&&!document.querySelector('#go').disabled",timeout=30000);pg.wait_for_timeout(400)
        r=pg.evaluate("({km:S.loopG.km,calm:S.loopG.calm,busy:S.loopG.busy,amb:S.loopG.amb})")
        print('amb',i,'km %.1f'%r['km'],'calm',r['calm'],'cible',r['amb']['target'],'atteint',r['amb']['met'],'candidats',r['amb']['calms'],'| appels ORS',calls['ors'],'dont lourds',calls['heavy'],'avec évitement',calls['avoid'])
        best=pg.evaluate("S.loopG.amb.calms")
    pg.evaluate("ready=true;S.gen=true;drawMap(true);osmStats()")
    print('ligne ambiance :',pg.evaluate("(document.getElementById('osm_amb')||{}).textContent"))
    print('erreurs',errs)
