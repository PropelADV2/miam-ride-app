import json,math
from playwright.sync_api import sync_playwright
calls={'ovp':0,'ors':0}
def ors(route):
    calls['ors']+=1;b=json.loads(route.request.post_data);co=b['coordinates']
    pts=[]
    for i in range(len(co)-1):
        for k in range(20):
            t=k/20;pts.append([co[i][0]+(co[i+1][0]-co[i][0])*t,co[i][1]+(co[i+1][1]-co[i][1])*t,100+8*math.sin(len(pts)/4)])
    pts.append(co[-1]+[100]);n=len(pts);heavy=bool(b.get('elevation'))
    ex={'waytypes':{'values':[[0,n//4,6],[n//4,n//2,3],[n//2,3*n//4,1],[3*n//4,n-1,4]]},'surface':{'values':[[0,n//2,3],[n//2,n-1,11]]}} if heavy else {}
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':[{'geometry':{'coordinates':pts},'properties':{'summary':{'distance':60000,'duration':9000},'extras':ex}}]}))
def ovp(route):
    calls['ovp']+=1
    els=[{'type':'node','id':i,'lat':48.74+0.02*(i%12),'lon':1.98+0.03*(i//12),'tags':{'name':'B%d'%i,'opening_hours':'Mo,We-Fr 07:00-19:30; Sa 08:00-13:00'}} for i in range(80)]
    els.append({'type':'way','id':900,'center':{'lat':48.74,'lon':1.98},'tags':{'name':'B0'}})  # doublon
    els.append({'type':'node','id':901,'lat':48.80,'lon':2.13,'tags':{'shop':'bakery'}})        # sans nom
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'elements':els}))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/overpass*/**',ovp);pg.route('**/maps.mail.ru/**',ovp)
    pg.goto('file:///mnt/user-data/outputs/miam-ride-osm-reel.html');pg.wait_for_timeout(600)
    pg.evaluate("localStorage.setItem('mr_osm','1');localStorage.setItem('mr_orskey','K');localStorage.removeItem('mr_bakc')");pg.reload();pg.wait_for_timeout(600)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300);pg.get_by_text('Plus tard',exact=True).first.click()
    pg.wait_for_timeout(2500);print('préchauffage: appels Overpass',calls['ovp'])
    # horaires
    print('horaires',pg.evaluate("""[osmHours('Mo,We-Fr 07:00-19:30; Sa 08:00-13:00'),osmHours('Tu-Su 07:00-13:00,15:30-19:30; PH off'),osmHours('Sa-Mo 08:00-12:00'),osmHours('sunrise-sunset'),osmHours('Mo-Su 06:30-20:00')].map(h=>h?h.map(d=>d.length).join(''):null)"""))
    o0=calls['ovp']
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_function("S.loopG&&!document.querySelector('#go').disabled",timeout=20000);pg.wait_for_timeout(800)
    print('générer: appels Overpass en plus',calls['ovp']-o0,'| bakeries',pg.evaluate("ALL.length"),'| doublon/sans nom exclus',pg.evaluate("ALL.filter(b=>b[0]==='B0').length+' B0 ; sansnom '+ALL.filter(b=>b[0]==='Boulangerie').length"))
    print('détail',pg.evaluate("document.getElementById('osm_det')?document.getElementById('osm_det').textContent:'(absent)'"))
    print('segments',pg.evaluate("S.loopG.segs.map(s=>s.calm).join('')"))
    pg.evaluate("ready=true;drawMap(true)")
    print('erreurs',errs)
