import json,sys
from playwright.sync_api import sync_playwright
def enc(pts):
    out='';la=lo=0
    for a,b in pts:
        A,B=round(a*1e5),round(b*1e5)
        for d in (A-la,B-lo):
            v=~(d<<1) if d<0 else d<<1
            while v>=32: out+=chr((32|(v&31))+63); v>>=5
            out+=chr(v+63)
        la,lo=A,B
    return out
import math
def circ(km):
    r=km/(2*math.pi)/1.3*1.0
    return [(48.8049+ (r*math.sin(t))/110.57, 2.1204+(r*(1-math.cos(t)))/73.3) for t in [i*math.pi/20 for i in range(41)]]
calls=[]
def route(r):
    u=r.request.url
    if 'computeRoutes' in u:
        b=json.loads(r.request.post_data); calls.append(('route',len(b['intermediates']),b['travelMode']))
        n=len(b['intermediates']); km=60 if n==4 else 62
        r.fulfill(json={'routes':[{'distanceMeters':km*1000,'duration':'9000s','polyline':{'encodedPolyline':enc(circ(km))}}]})
    elif 'searchNearby' in u:
        b=json.loads(r.request.post_data); c=b['locationRestriction']['circle']['center']; calls.append(('near',b['includedTypes']))
        i=len(calls)
        r.fulfill(json={'places':[{'id':'g%d_%d'%(i,k),'displayName':{'text':'Boulangerie Stub %d-%d'%(i,k)},'formattedAddress':'1 rue Test','location':{'latitude':c['latitude']+0.003*k,'longitude':c['longitude']+0.003},'rating':4.6,'userRatingCount':120+k,'regularOpeningHours':{'periods':[{'open':{'day':d,'hour':6,'minute':30},'close':{'day':d,'hour':20,'minute':0}} for d in range(7)]}} for k in range(4)]})
    else: r.continue_()
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-sandbox']);
    for f in ['accueil-velo.html','miam-ride-osm.html','introduction-miam-ride.html']:
        pg=b.new_page(viewport={'width':430,'height':900}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.route('**/*',route); calls.clear()
        pg.goto('file:///mnt/user-data/outputs/'+f); pg.wait_for_timeout(500)
        print(f,'load errs',errs)
        if f.startswith('intro'): continue
        # demo mode unaffected
        n0=pg.evaluate('ALL.length'); pg.evaluate("document.querySelector('#intro')&&document.querySelector('#intro').remove()"); pg.click('#go'); pg.wait_for_timeout(300); print('demo ok',pg.evaluate('S.gen'),calls)
        # google mode
        pg.evaluate("PLACES_CONFIG.provider='google';PLACES_CONFIG.googleKey='K'")
        pg.evaluate("document.querySelector('#go').hidden=false;S.gen=false;S.traced=false")
        pg.click('#go',force=True); pg.wait_for_timeout(800)
        print('calls',calls[:8]); print('ALL',pg.evaluate('ALL.length'),pg.evaluate('ALL[0]'),'loopKm',pg.evaluate('S.loopG&&S.loopG.km'),'notice',pg.evaluate('S.notice'))
        pg.evaluate("S.picks=[];") 
        print('cands',pg.evaluate('cands(0).list.length'),'gen',pg.evaluate('S.gen'))
        for j in range(pg.evaluate('S.np')):
            pg.evaluate('choose(cands(S.active).list[0])')
        pg.wait_for_timeout(800); print('full',pg.evaluate('S.full'),'traced',pg.evaluate('S.traced'))
        pass
        print('final calls',calls,'routeG km',pg.evaluate('S.routeG&&S.routeG.km'),'stops',pg.evaluate('S.routeG&&S.routeG.stops.length'),'traced',pg.evaluate('S.traced'))
        print('errs',errs)
    b.close()
