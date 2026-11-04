import json,math
from playwright.sync_api import sync_playwright
def hav(a,b):
    R=6371;dl=math.radians(b[1]-a[1]);dg=math.radians(b[0]-a[0]);x=math.sin(dl/2)**2+math.cos(math.radians(a[1]))*math.cos(math.radians(b[1]))*math.sin(dg/2)**2
    return 2*R*math.asin(math.sqrt(x))
calls={'ors':0,'ovp':0,'bodies':[]}
def ors(route):
    calls['ors']+=1;b=json.loads(route.request.post_data);calls['bodies'].append(b)
    co=b['coordinates']
    if abs(co[0][1]-48.8030)<1e-6 and calls['ors']%3==2:
        return route.fulfill(status=404,headers={'access-control-allow-origin':'*','content-type':'application/json'},body='{"error":{"code":2009,"message":"Route could not be found - Unable to find a route between points 1 (2.13 48.80) and 2 (2.14 48.80)"}}')

    if route.request.headers.get('authorization')!='KEY123':
        return route.fulfill(status=403,headers={'access-control-allow-origin':'*'},body='{"error":{"message":"denied"}}')
    pts=[]
    for i in range(len(co)-1):
        for k in range(20):
            t=k/20;pts.append([co[i][0]+(co[i+1][0]-co[i][0])*t,co[i][1]+(co[i+1][1]-co[i][1])*t,100+10*math.sin(len(pts)/5)])
    pts.append(co[-1]+[100])
    d=sum(hav(pts[i],pts[i+1]) for i in range(len(pts)-1))*1.3*1000
    n=len(pts)
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'features':[{'geometry':{'coordinates':pts},'properties':{'summary':{'distance':d,'duration':d/6},'extras':{'waytypes':{'values':[[0,n//2,3],[n//2,n-1,1]]}}}}]}))
def ovp(route):
    calls['ovp']+=1
    els=[{'type':'node','id':i,'lat':48.74+0.02*(i%12),'lon':1.98+0.03*(i//12),'tags':{'name':f'Boulangerie Test {i}','shop':'bakery','opening_hours':'Mo-Sa 07:00-19:30; Su 07:00-13:00','addr:street':'rue Royale','addr:housenumber':str(i)}} for i in range(1,80)]
    route.fulfill(headers={'access-control-allow-origin':'*','content-type':'application/json'},body=json.dumps({'elements':els}))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);pg=b.new_page(viewport={'width':400,'height':860});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/api.openrouteservice.org/**',ors);pg.route('**/overpass-api.de/**',lambda r:r.fulfill(status=503,headers={'access-control-allow-origin':'*'},body='busy'));pg.route('**/overpass.kumi.systems/**',ovp)
    pg.goto('file:///mnt/user-data/outputs/miam-ride-osm-reel.html#demo');pg.wait_for_timeout(800)
    pg.get_by_text('Passer',exact=True).first.click();pg.wait_for_timeout(300)
    pg.get_by_text('Plus tard',exact=True).first.click();pg.wait_for_timeout(300)
    pg.evaluate("document.querySelectorAll('.tabbar button')[5].click()");pg.wait_for_timeout(300)
    pg.evaluate("[...document.querySelectorAll('#pmenu .row')].find(r=>r.innerText.includes('Compte')).click()");pg.wait_for_timeout(300)
    pg.fill('#osm_key','KEY123');pg.select_option('#osm_on','1');pg.click('#osm_test');pg.wait_for_timeout(600)
    print('test clé:',pg.inner_text('#osm_msg'))
    pg.fill('#osm_key','BAD');pg.click('#osm_test');pg.wait_for_timeout(500);print('mauvaise clé:',pg.inner_text('#osm_msg'))
    pg.fill('#osm_key','KEY123');pg.click('#osm_test');pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('.tabbar button')[0].click()");pg.wait_for_timeout(300)
    pg.evaluate("document.querySelector('#go').click()");pg.wait_for_timeout(2500)
    print('loop km',pg.evaluate("S.loopG&&S.loopG.km"),'ALL',pg.evaluate("ALL.length"),'BAK',pg.evaluate("BAK.length"),'ors',calls['ors'],'ovp',calls['ovp'])
    print('notice',pg.evaluate('S.notice'),pg.evaluate('S.gen'),pg.evaluate('OSMC.list.length'),pg.evaluate('JSON.stringify(OSMC.bb)'),pg.evaluate('JSON.stringify(S.loopG.path.slice(0,2))'))
    print('dbg',pg.evaluate("(async()=>{const pt=pointAtPct(S.loopG.path,.4);const r=await PlacesGoogle.near(pt,2500);return [JSON.stringify(pt),r.length,typeof gPrepare, gOn()]})()"))
    print('candidats',pg.evaluate("cands(0).list.map(b=>b[0]+' '+note(b)).slice(0,3)"))
    pg.evaluate("choose(cands(0).list[0])");pg.wait_for_timeout(1500)
    print('full',pg.evaluate("S.full"),'routeG',pg.evaluate("!!S.routeG"),'ors',calls['ors'],'stats',pg.inner_text('#stats').replace('\n',' '))
    print('hours',pg.evaluate("Object.keys(HRS).filter(k=>k.startsWith('Boulangerie Test')).length"),'markers',pg.evaluate("markers.length"))
    pg.evaluate('ready=true;drawMap(true)');pg.wait_for_timeout(300);print('markers',pg.evaluate('markers.length'),'maplibre stub',pg.evaluate('typeof maplibregl.Map'))
    print('summary km',pg.evaluate('S.cur.km'))
    print('chrono',pg.evaluate("document.getElementById('osm_time').textContent"),'lf',pg.evaluate('PLACES_CONFIG.loopFactor'))
    pg.screenshot(path='osm1.png');print(errs)
